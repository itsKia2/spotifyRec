import spotipy
from spotipy import SpotifyOAuth


def connectClient(user):
    with open("secret.txt") as f:
        secret_ls = f.readlines()
        # -1 makes sure we dont get terminating value
        spotipy_client_id = secret_ls[0][:-1]
        spotipy_secret = secret_ls[1][:-1]

    spAuth = SpotifyOAuth(
        client_id=spotipy_client_id,
        client_secret=spotipy_secret,
        redirect_uri="http://localhost:8888/callback",
        scope="user-library-read",
        username=user,
        show_dialog=True,
    )
    sp = spotipy.Spotify(auth_manager=spAuth)
    return sp
