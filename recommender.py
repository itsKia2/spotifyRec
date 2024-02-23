import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import textblob
from textblob import TextBlob
from textblob.blob import TextBlob

def processAllSongs():
    pldf = importProcessed()
    pldf = selectFeatureCols(pldf)
    pldf = processGenreList(pldf)
    floatCols = float_cols = pldf.dtypes[pldf.dtypes == 'float64'].index.values
    pldf.to_csv("./data/allsong_data.csv", index = False)
    finalDF = create_feature_set(pldf, float_cols=floatCols)
    finalDF.to_csv("./data/completeFeature.csv", index=False)
    print(finalDF)

def importProcessed():
    playlistDF = pd.read_csv("./data/processed_data.csv")
    playlistDF.drop(columns=["Unnamed: 0",'Unnamed: 0.1'], inplace = True)
    return playlistDF

def selectFeatureCols(df):
    return df[['artist','id','track_name','danceability', 'energy', 'key', 'loudness', 'mode',
              'speechiness', 'acousticness', 'instrumentalness', 'liveness',
              'valence', 'tempo', "artist_pop", "genres", "track_pop"]]

def processGenreList(df):
    df['genres_list'] = df['genres'].apply(lambda x: x.split(" "))
    return df


def getSubjectivity(text):
    # Getting the Subjectivity using TextBlob
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    # Getting the Polarity using TextBlob
    return TextBlob(text).sentiment.polarity

def getAnalysis(score, task="polarity"):
    # Categorizing the Polarity & Subjectivity score
    if task == "subjectivity":
        if score < 1/3:
            return "low"
        elif score > 1/3:
            return "high"
        else:
            return "medium"
    else:
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

def sentiment_analysis(df, text_col):
    df['subjectivity'] = df[text_col].apply(getSubjectivity).apply(lambda x: getAnalysis(x,"subjectivity"))
    df['polarity'] = df[text_col].apply(getPolarity).apply(getAnalysis)
    return df

def ohe_prep(df, column, new_name):
    tf_df = pd.get_dummies(df[column])
    feature_names = tf_df.columns
    tf_df.columns = [new_name + "|" + str(i) for i in feature_names]
    tf_df.reset_index(drop = True, inplace = True)
    return tf_df

def tfidfImp(df):
    tfidf = TfidfVectorizer()
    tfidf_matrix =  tfidf.fit_transform(df['genres_list'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names_out()]
    # if genre_df.get("genre|unknown") != None:
        # genre_df.drop(columns='genre|unknown')
    genre_df.reset_index(drop = True, inplace=True)
    return genre_df

def normalize(df):
    pop = df[["artist_pop"]].reset_index(drop = True)
    scaler = MinMaxScaler()
    pop_scaled = pd.DataFrame(scaler.fit_transform(pop), columns = pop.columns)
    return pop_scaled

def create_feature_set(df, float_cols):
    # Tfidf genre lists
    tfidf = TfidfVectorizer()
    tfidf_matrix =  tfidf.fit_transform(df['genres_list'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names_out()]
    genre_df.drop(columns='genre|unknown') # drop unknown genre
    genre_df.reset_index(drop = True, inplace=True)

    # Sentiment analysis
    df = sentiment_analysis(df, "track_name")

    # One-hot Encoding
    subject_ohe = ohe_prep(df, 'subjectivity','subject') * 0.3
    polar_ohe = ohe_prep(df, 'polarity','polar') * 0.5
    key_ohe = ohe_prep(df, 'key','key') * 0.5
    mode_ohe = ohe_prep(df, 'mode','mode') * 0.5

    # Normalization
    # Scale popularity columns
    pop = df[["artist_pop","track_pop"]].reset_index(drop = True)
    scaler = MinMaxScaler()
    pop_scaled = pd.DataFrame(scaler.fit_transform(pop), columns = pop.columns) * 0.2
    # Scale audio columns
    floats = df[float_cols].reset_index(drop = True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns = floats.columns) * 0.2
    # Concanenate all features
    final = pd.concat([genre_df, floats_scaled, pop_scaled, subject_ohe, polar_ohe, key_ohe, mode_ohe], axis = 1)
    # Add song id
    final['id']=df['id'].values
    return final
