import spotipy
from spotipy import SpotifyOAuth
from playlist import *

with open("secret.txt") as f:
    secret_ls = f.readlines()
    spotipy_client_id = secret_ls[0][:-2]
    spotipy_secret = secret_ls[1]

print(spotipy_client_id)
print(spotipy_secret)

spAuth = SpotifyOAuth(
    client_id=spotipy_client_id,
    client_secret=spotipy_secret,
    redirect_uri="http://localhost:8888/callback",
    username="itsKia2",
    # scope=SCOPE,
    show_dialog=True,
    # cache_path=CACHE,
)
print("Success")

sp = spotipy.Spotify(auth_manager=spAuth)
