import spotipy
from client import *
from playlist import *

sp = connectClient()
df = tracksFromPlaylist(sp, "itKia", "7pr3rDzikgmaNDpS1sgk6V")
