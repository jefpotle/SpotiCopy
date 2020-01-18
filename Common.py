import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# get the username
username = sys.argv[1]
scope = 'user-library-read'

# authorization
try:
    token = util.prompt_for_user_token(username, scope, client_id = 'c2efa581fbab458baaec0d6cb22664da', client_secret = '', redirect_uri = 'http://google.com/') # insert client secret ID
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope, client_id = 'c2efa581fbab458baaec0d6cb22664da', client_secret = '', redirect_uri = 'http://google.com/') # insert client secret ID

# create spotipy object
spotify = spotipy.Spotify(auth = token)

# getting all public playlists from user
results = spotify.user_playlists(username)
hash = {}
for playlist in results['items']:
    print(playlist["name"])
    hash[playlist["name"]] = playlist["id"]

# grabbing input from user
playlists = ""
while(playlists != "exit"):
    playlists = input('\nPlease enter the playlists you would want to look at, seperated by ",": ')
    playlists = playlists.split(", ")

    def individualTracks(playlistName):

        # grabbing the data
        list = []
        for i, item in enumerate(playlistName["items"]):
            track = item["track"]
            temp = str(track["name"] + " by: " + track['artists'][0]['name'])
            list.append(temp)
        return (list)

    # grabbing tracks from the playlists
    total = []
    for x in playlists:
        tracks = spotify.user_playlist(username, playlist_id = hash[x], fields = "tracks, next")
        tracks = (tracks["tracks"])
        total.append(individualTracks(tracks))

    # final algorithm
    aggregate = []
    for x in total:
        for y in x:
            aggregate.append(y)

    final = []
    for x in aggregate:
        if aggregate.count(x) == len(total):
            final.append(x)
    final = set(final)

    # printing output
    print("\nThese are the songs that are in all of these playlists: \n")
    for x in final:
        print(x)
