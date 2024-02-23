import re
import pandas as pd
from tqdm import tqdm

def extractFeat(sp, dataset):
    dataPath = dataset
    df = pd.read_csv(dataPath)
    # df.head()
    # Edit the track-uris to a more usable format
    df["track_id"] = df["track_id"].apply(lambda x: re.findall(r'\w+$', x)[0])
    df["track_id"]
    testDF = df
    ariFeatures(sp, df["track_id"][0])
    first_half = df["track_id"].unique()[:10000]
    second_half = df["track_id"].unique()[10000:20000]
    third_half = df["track_id"].unique()[20000:]
    dataLIST = [first_half,second_half,third_half]
    featureLIST = []
    for i in tqdm([id for id in dataLIST[0]]):
        try:
            featureLIST.append(ariFeatures(sp, i))
        except:
            continue
    for i in tqdm([id for id in dataLIST[1]]):
        try:
            featureLIST.append(ariFeatures(sp, i))
        except:
            continue
    for i in tqdm([id for id in dataLIST[2]]):
        try:
            featureLIST.append(ariFeatures(sp, i))
        except:
            continue
    featureDF = pd.DataFrame(featureLIST)
    new_df = pd.merge(testDF,featureDF, left_on = "track_id", right_on= "id")
    new_df.to_csv('./data/processed_data.csv')

def ariFeatures(sp, ari):
    features = sp.audio_features(ari)[0]
    #Artist of the track, for genres and popularity
    artist = sp.track(ari)["artists"][0]["id"]
    artist_pop = sp.artist(artist)["popularity"]
    artist_genres = sp.artist(artist)["genres"]
    #Track popularity
    track_pop = sp.track(ari)["popularity"]
    #Add in extra features
    features["artist_pop"] = artist_pop
    if artist_genres:
        features["genres"] = " ".join([re.sub(' ', '_', i) for i in artist_genres])
    else:
        features["genres"] = "unknown"
    features["track_pop"] = track_pop

    return features
