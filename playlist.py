import pandas as pd

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


def mySavedTracks(sp):
    response = sp.current_user_saved_tracks(limit=50)
    counter = 0
    for item in response["items"]:
        track = item["track"]
        print("%d - %32.32s %s" % (counter, track["artists"][0]["name"], track["name"]))
        counter = counter + 1


def tracksFromPlaylist(sp, creator, pID):
    # Create empty dataframe
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
