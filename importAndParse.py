#DEFAULT PACKAGE IMPORTS
import json

#FILE IMPORTS
import createOutput as co
import cacheManager as sCache

# RATE LIMIT IS 50 SONGS PER BATCH CALL
# MAX CALLS IS 30 PER SECOND, THROTTLE FOR LARGE SCALE
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


def dataFileRead(inFileName):
    """
    This function takes an input json file and returns the data on every indvidual steam.
    It also populates the global varable songDatabase with the relevant song data from the API.
    Args:
        inFileName (str): the name of a json file formatted as detailed in $makeAFileFormatFile$, without the .json at the end of the string.
    Returns:
        streams (dict): the dict holding information on all streams, keyed by stream date.
    
    """
    inFile = 'Data/'+inFileName+'.json'
    with open(inFile) as f:
        dataRead = json.load(f)
    
    # dict will hold information on every stream in the input file, indexed by streamdate
    streams = dict()

    for value in dataRead:
        # if stream is not a song, next stream
        if (value['spotify_track_uri'] is None or value['spotify_track_uri'] == None) : continue

        # add relevant stream information to streams dict
        streamDate = value['ts']
        streamURI = value['spotify_track_uri']
        streamDuration = int(value['ms_played'])
        skipped = bool(value['skipped'])
        streams.update({streamDate:{'uri':streamURI, 'duration':streamDuration, 'skip':skipped}})
            
    return streams


# TODO: finish this documentation stub
def parseStreams(streamData:dict):
    """
    Given streamData this function queries the spotipy API and returns a dict containing on
    all songs streamed, avoiding redundant calls.
    """

    #get whatever is currently stored in the cache
    songDatabase:dict = sCache.readCache()

    unknownSongURI = set()
    
    for stream in streamData.values():
        curSongURI = stream['uri']
        if curSongURI not in songDatabase.keys():
            unknownSongURI.add(curSongURI)
            
            #querey once 50 songs is set for the batch call
            if(len(unknownSongURI) == 50):
                songDatabase.update(quereyAPI(unknownSongURI))
                unknownSongURI.clear()
    
    #querey remaining songs
    songDatabase.update(quereyAPI(unknownSongURI))
    
    return songDatabase



def quereyAPI(uris:set):
    """
    Queries the api for a batch call of track information.
    Throtles itself to only 1500 calls per rolling 30 second window
    using a global quereyTracker object. Updates the song data cache.
    Args:
        uris (set): Set of URI's for the batch query.
    Returns:
        Out (dict): Formatted dictionary of song data by keyed by URI retreved from query.
    """
    
    #dummy check
    if len(uris) == 0:
        return {}

    #ACTUAL QUEREY, needs to be throttled
    songImports = sp.tracks(uris)['tracks']
    
    songData = dict()

    #parse recieved data
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
        songData.update({ uri:{'name':name, 'album':albumName, 'artists':artistsString, 'coverURL':albumCoverURL, 'duration':songDuration} })


    sCache.updateCache(songData)
    return songData


def organizeByPercentage(streamData:dict, songData:dict):
    """
    This function creates an output html file that holds all songs in the given data using the
    imported song data. The songs in the html file are organized by total percentage of song
    listening time (ie if a song is 3 minutes and it was listened to for a total of 9 minutes 
    the total % time would be 300).
    Args:
        streamData (dict): Data on all streams as parsed by function dataFileRead()
        songData (dict): Cached data on all streams as created and managed by INSERT CACHE MANAGER HERE
    """
    # this will be passed to the helper function to create the html code
    songPercentagesDict = dict()
    for stream in streamData.values():
        song = songData[stream['uri']]
        curPercent = songPercentagesDict.get(stream['uri'], 0.0)
        curPercent += float(song['duration'])/float(stream['duration'])
        songPercentagesDict.update({stream['uri']:curPercent})
    
    songPercentages = []
    for uri, percent in songPercentagesDict.items():
        curSong = songData[uri]
        print(percent, " : ", str(int(percent)))
        songPercentages.append((curSong['name'], curSong['artists'], curSong['album'], curSong['coverURL'], (int(percent))))
    songPercentages = sorted(songPercentages, key=lambda x: x[4], reverse=True)
    co.createOutputFile(songPercentages, "Songs by Total Percentage Listened", "percentOutput")
#main



streamData  = dataFileRead('test')
songData = parseStreams(streamData)
organizeByPercentage(streamData, songData)

