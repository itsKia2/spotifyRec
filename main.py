from client import *
from playlist import *
from ari import *

creator = "itsKia2"
url = getPlaylistID(
    "https://open.spotify.com/playlist/1IjnMCB8vrBAgVl3BWaiQ7?si=dfcab64aad714bbc"
)

# pid = getPlaylistID(url)

sp = connectClient(creator)
# mySavedTracks(sp)
# tracksFromPlaylist(sp, creator, url)
# mySavedTracks(sp)
extractFeat(sp, "./data/likedSongs.csv")
