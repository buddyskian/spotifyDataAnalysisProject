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
    print(codes[2])

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)



#read spotify streaming history file and return
# dict() holding all the streams and their relevant information
# dict() holding all the songs streamed and the information aquried from the api call
#TODO: fix the docstrings for this funciton, possibly split into two functions for readability
def dataFileRead(inFileName):
    """
    This function takes an input json file and returns the data on every indvidual steam and the
    information on each song streamed from the spotify API.
    Args:
        inFileName (str): the name of a json file formatted as detailed in $makeAFileFormatFile$, without the .json at the end of the string.
    Returns:
        tuple (dict(), dict()): A tuple containing:
            -streams : the dict holding information on all streams, keyed by stream date.
            -songDatabase : the dict holding information on all streams, keyed by stream date.
    
    """
    inFile = 'Data/'+inFileName+'.json'
    with open(inFile) as f:
        dataRead = json.load(f)
    
    #dict will hold information on every stream in the input file, indexed by streamdate
    streams = dict()
    
    #set that will be used for the api batch call, holds songURIs
    allSongURI = set()

    #will hold the data aquired from spotipy API calls, indexed by songURI
    songDatabase = dict() #songURI:(name,albumName,artists,albumCoverURL,duration)
    for value in dataRead:
        #if stream is not a song, next stream
        if (value['spotify_track_uri'] is None or value['spotify_track_uri'] == None) : continue

        #add relevant stream information to streams dict
        #TODO: make this into a function



        #add song to the cache for the batch call to the spotipy API 
        #this avoids redundant calls
        allSongURI.add(value['spotify_track_uri'])
        

    #While this batch call avoids redundant calls, it doesn't limit itself to 50 calls at a time
    #TODO: Limit number of calls per batch to 50 and limit number of calls/second to 50
    songImports = sp.tracks(allSongURI)['tracks']
    
    #fill songDatabase, could be made into a separate function later
    #TODO: Make this into a callable function most likely
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
