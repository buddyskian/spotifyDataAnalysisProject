outputStartStr = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Spotify Data</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div class="app-shell">
    <header class="app-header">
      <h1>{}</h1>
      <p>Generated using Python + Spotify API</p>
    </header>

    <main class="song-list">"""

outputEndStr = """</main>
  </div>

</body>
</html>"""

middleStrSkeleton = """<div class="song-row">
        <img class="song-cover" src="{}" alt="Album Cover" />

        <div class="song-info">
          <div class="song-title">{}</div>
          <div class="song-artist">{} / {}</div>
        </div>

        <div class="song-data">{}</div>
      </div>"""

#this function will take an ordered list of tuples of song information and create an
#output html file that holds the song information in a pretty way
#inSongs :: {(SongName, SongAlbum, SongArtist, SongAlbumCover, Data)}
#SongName::string
#SongArtist::string
#SongAlbum::string
#SongAlbumCover::URL
#Data::string/int/double/float (will be cast to string)
#DataType::String
def createOutputFile(inSongs, DataType="Song Length"):
    outputMiddleStr = ""
    for song in inSongs:
        outputMiddleStr += middleStrSkeleton.format(song[3], song[0], song[2], song[1], str(song[4]))
    with open("createdOutput.html", 'w') as f:
        f.write(outputStartStr.format(DataType)+outputMiddleStr+outputEndStr)
    return


#TesterCode to make sure that this works
"""
testList =  [("Bags", "Immunity", "Clairo", "https://upload.wikimedia.org/wikipedia/en/5/56/Clairo_-_Immunity.png", "3:20"),
             ("Alewife", "Immunity", "Clairo", "https://upload.wikimedia.org/wikipedia/en/5/56/Clairo_-_Immunity.png", "4:10") ]
createOutputFile(testList)
"""