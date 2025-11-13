import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your actual Client ID and Client Secret
with open('APICodes.json') as codeFile:
    codes = json.load(codeFile)
    CLIENT_ID = codes['clientid']
    CLIENT_SECRET = codes['secretid']


# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def dataFileRead(inFileName):
    inFile = 'Data/'+inFileName+'.json'
    with open(inFile) as f:
        dataRead = json.load(f)
    parsedData = dict()
    for value in dataRead:
        curTrack = value['master_metadata_track_name']
        if (value['spotify_track_uri'] is None or value['spotify_track_uri'] == None) : continue
        parsedData.update({curTrack: parsedData.get(curTrack, 0)+1})
        print(curTrack, ":", value['spotify_track_uri'])
        trackTime = sp.track(value['spotify_track_uri'])['duration_ms']
        print(curTrack, ":", trackTime)

    print(parsedData)
    return True

#main
dataFileRead('test')
