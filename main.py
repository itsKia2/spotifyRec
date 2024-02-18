import spotipy
from spotipy import SpotifyClientCredentials

cid = "8748b5774c754f0299f292b89d45c1cc"
secret = "be8ca0d5eee147fdba4113c70b3f7876"

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# results = sp.current_user_saved_tracks()
playlists = sp.user_playlists("spotify")
while playlists:
    for i, playlist in enumerate(playlists["items"]):
        print(
            "%4d %s %s"
            % (i + 1 + playlists["offset"], playlist["uri"], playlist["name"])
        )
    if playlists["next"]:
        playlists = sp.next(playlists)
    else:
        playlists = None
