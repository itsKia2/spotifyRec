import spotipy
from spotipy import SpotifyClientCredentials
import pandas as pd

with open("secret.txt") as f:
    secret_ls = f.readlines()
    spotipy_client_id = secret_ls[0][:-2]
    spotipy_secret = secret_ls[1]

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=spotipy_client_id,
        client_secret=spotipy_secret,
    )
)


def getPlaylist(creator, pID):
    # Create empty dataframe
    playlist_features_list = [
        "artist",
        "album",
        "track_name",
        "track_id",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature",
    ]

    playlist_df = pd.DataFrame(columns=playlist_features_list)

    # Loop through every track in the playlist, extract features and append the features to the playlist df

    playlist = sp.user_playlist_tracks(creator, pID)["items"]
    for track in playlist:  # Create empty dict
        playlist_features = {}  # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]

        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]

        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index=[0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)

    return playlist_df


df = getPlaylist("itsKia2", "7pr3rDzikgmaNDpS1sgk6V")
