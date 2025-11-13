CURRENT PLAN FOR DATA RELATIONS OF PROJECT:
streams: [holds all streams in the given database]
    streamdate::string (key)
    streamsong::string [songname]
    URI::string (foreign key: songDatabase, songStreams)
    streamlength::int [length of this stream in milliseconds]
    streamendreason::string [songend, skpbtn, pausebutton]

songDatabase: [created via batch calls to spotipy API using caches to avoid redundancy]
    URI::string (key)
    songlength::int [milliseconds]
    songname::string
    songalbum::string

songSteams:
    URI (key)
    songname::string
    streams::int [number of times the song has begun streaming]
    streamMills::int [total ammount of time song has been streamed in milliseconds] 
