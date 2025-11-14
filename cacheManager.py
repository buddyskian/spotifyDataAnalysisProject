###############################################
# THIS FILE IS USED FOR MANAGING A PERSISTANT #
# CAHCE OF IMPORTED SONG DATA, STORED IN A    #
# JSON FILE, songDataCache.json               #
###############################################

import json
from pathlib import Path

filePath = Path('songDataCache.json')


def readCache():
    """
    Reads the data from songDataCache.json and returns it as 
    a dict. Should be called once for every run of the code.
    """
    cacheData = dict()
    
    if filePath.is_file():
        with open(filePath, 'r') as f:
            cacheData = json.load(f)
        return cacheData
    else:
        return {}


def updateCache(importedData:dict):
    """
    Given a dict of new song data this function updates
    songDataCache.json with all needed information. Should be called
    after every single API call is made.
    Args:
        importedData (dict): All data new or old from the api.
    """
    cacheData = dict()
    
    if filePath.is_file():
        with open(filePath, 'r') as f:
            cacheData = json.load(f)
    else:
        cacheData = {}
    cacheData.update(importedData)
    with open(filePath, 'w') as f:
        json.dump(cacheData, f, indent=4)
