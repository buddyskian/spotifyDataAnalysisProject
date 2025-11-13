import json
import createOutput as co

#RATE LIMIT IS 50 SONGS PER BATCH CALL
#MAX CALLS IS 30 PER SECOND, THROTTLE FOR LARGE SCALE
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# API Keys are pulled from json file to avoid leaking to github
# IMPORTANT: make sure to switch between keys from the file to avoid hitting rate limits
with open('APICodes.json') as codeFile:
    codes = json.load(codeFile)
    CLIENT_ID = codes[2]['clientid']
    CLIENT_SECRET = codes[2]['secretid']

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


#TODO: fix this documentation stub
def dataFileRead(inFileName):
    """
    This function takes an input json file and returns the data on every indvidual steam.
    It also populates the global varable songDatabase with the relevant song data from the API.
    Args:
        inFileName (str): the name of a json file formatted as detailed in $makeAFileFormatFile$, without the .json at the end of the string.
    Returns:
        streams (dict): the dict holding information on all streams, keyed by stream date. \n {streamDate:()}
    
    """
    inFile = 'Data/'+inFileName+'.json'
    with open(inFile) as f:
        dataRead = json.load(f)
    
    #dict will hold information on every stream in the input file, indexed by streamdate
    streams = dict()

    for value in dataRead:
        #if stream is not a song, next stream
        if (value['spotify_track_uri'] is None or value['spotify_track_uri'] == None) : continue

        #add relevant stream information to streams dict
        streamDate = value['ts']
        streamURI = value['spotify_track_uri']
        streamDuration = int(value['ms_played'])
        skipped = bool(value['skipped'])
        streams.update({streamDate:(streamURI, streamDuration, skipped)})
            
    return streams


#TODO: Throttle this function to avoid hitting the API call limit
#TODO: finish this documentation stub
def quereyAPI(streamData):
    """
    Given streamData this function queries the spotipy API and returns a dict containing on
    all songs streamed, avoiding redundant calls.
    """

    allSongURI = set()

    for stream in streamData.values():
        allSongURI.add(stream[0])
    
    #While this batch call avoids redundant calls, it doesn't limit itself to 50 calls at a time
    #TODO: HERE IS THE PLACE TO THROTTLE
    songImports = sp.tracks(allSongURI)['tracks']
    
    songDatabase = dict()

    for song in songImports:
        uri = song['uri']
        name = song['name']
        albumName = song['album']['name']
        songDuration = int(song['duration_ms'])
        artistsString = ""
        for artist in song['artists']:
            artistsString += artist['name'] + ", "
        artistsString = artistsString[:-2]
        albumCoverURL = song['album']['images'][0]['url']
        songDatabase.update({ uri:{'name':name, 'album':albumName, 'artists':artistsString, 'coverURL':albumCoverURL, 'duration':songDuration} })

    return songDatabase

#main
streamData  = dataFileRead('test')
songData = quereyAPI(streamData)

