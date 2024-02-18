import spotipy
from client import *
from playlist import *

sp = connectClient()
mySavedTracks(sp)
