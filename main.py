from client import *
from playlist import *
from ari import *
from recommender import *

creator = "itsKia2"
url = getPlaylistID(
    "https://open.spotify.com/playlist/1IjnMCB8vrBAgVl3BWaiQ7?si=dfcab64aad714bbc"
)

# pid = getPlaylistID(url)

sp = connectClient(creator)


# FIRST CHECK IF CSV FILES HAVE ALREADY BEEN CREATED BEFORE QUERYING SPOTIFY <----------------------------------------------
# mySavedTracks(sp)
# tracksFromPlaylist(sp, creator, url)
# mySavedTracks(sp)

extractFeat(sp, "./data/SHORTdataset.csv")
processAllSongs()
