import json
import createOutput as co
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your actual Client ID and Client Secret
with open('APICodes.json') as codeFile:
    codes = json.load(codeFile)
    CLIENT_ID = codes[2]['clientid']
    CLIENT_SECRET = codes[2]['secretid']
    print(codes[2])

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


#RATE LIMIT IS 50 SONGS PER BATCH CALL

def dataFileRead(inFileName):
    inFile = 'Data/'+inFileName+'.json'
    with open(inFile) as f:
        dataRead = json.load(f)
    parsedData = dict()
    #set that will be used for the api batch call
    allSongURI = set()
    songDatabase = dict() #songURI:(name,albumName,artists,albumCoverURL,duration)
    for value in dataRead:
        curTrack = value['master_metadata_track_name']
        if (value['spotify_track_uri'] is None or value['spotify_track_uri'] == None) : continue
        parsedData.update({curTrack: parsedData.get(curTrack, 0)+1})
        print(curTrack, ":", value['spotify_track_uri'])
        #Optimize this to not require calling the API every time
        #This will avoid hitting the rate limit and also hopfully prevent a need to multi thread.
        allSongURI.add(value['spotify_track_uri'])
        #trackTime = sp.track(value['spotify_track_uri'])['duration_ms']

    print(len(allSongURI), "\n\n")
    songImports = sp.tracks(allSongURI)['tracks']
    for song in songImports:
        uri = song['uri']
        name = song['name']
        albumName = song['album']['name']
        duration = int(song['duration_ms'])
        artistsString = ""
        for artist in song['artists']:
            artistsString += artist['name'] + ", "
        artistsString = artistsString[:-2]
        albumCoverURL = song['album']['images'][0]['url']
        songDatabase.update({uri:(name, albumName, artistsString, albumCoverURL, duration)})
    return True

#main
dataFileRead('test')
