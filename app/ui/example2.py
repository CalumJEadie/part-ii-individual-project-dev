# Smart Music Player

seed_videos = youtube.VideoCollection([
    # Pop
    "http://www.youtube.com/watch?v=9bZkp7q19f0", # PSY - GANGNAM STYLE
    "http://www.youtube.com/watch?v=lJqbaGloVxg", # James Arthur - Impossible - Official Single
    "http://www.youtube.com/watch?v=kYtGl1dX5qI", # will.i.am - Scream & Shout ft. Britney Spears
    "http://www.youtube.com/watch?v=bqIxCtEveG8", # Labrinth feat. Emeli Sande - Beneath Your Beautiful
    # Country
    "http://www.youtube.com/watch?v=KHF9itPLUo4", # Johnny Cash - I Walk the Line
    "http://www.youtube.com/watch?v=WA4iX5D9Z64", # Taylor Swift - We Are Never Ever Getting Back Together
    "http://www.youtube.com/watch?v=vNoKguSdy4Y", # Taylor Swift - I Knew You Were Trouble
    # Rap and Hip Hop
    "http://www.youtube.com/watch?v=j5-yKhDd64s", # Eminem - Not Afraid
    # Rock
    "http://www.youtube.com/watch?v=DF0zefuJ4Ys", # The Fray - How to save a life (lyrics)
    "http://www.youtube.com/watch?v=hLQl3WQQoQ0", # Adele - Someone Like You
    "http://www.youtube.com/watch?v=pY9b6jgbNyc", # Coldplay - Fix You
    # Electronic
    "http://www.youtube.com/watch?v=uweWiCLT8Eg", # David Guetta - She Wolf (Lyrics Video) ft. Sia
    "http://www.youtube.com/watch?v=1y6smkh6c-0", # Don't You Worry Child (Live)
    "http://www.youtube.com/watch?v=qimiWfZAtXw", # Wiley | Heatwave feat. Ms.D (Official Video)
    "http://www.youtube.com/watch?v=YJVmu6yttiw", # SKRILLEX - Bangarang feat. Sirah [Official Music Video]
    # Folk
    "http://www.youtube.com/watch?v=FOjdXSrtUxA", # Ed Sheeran - Give Me Love [Official Video]
    "http://www.youtube.com/watch?v=4A3poKE6qnM", # Lenka - Everything At Once
    "http://www.youtube.com/watch?v=p1iDBtcEm0w", # Stubborn Love by The Lumineers (Lyric Video)
    # Metal
    "http://www.youtube.com/watch?v=v_09wFxoaeQ", # Slipknot - Before I Forget
    # Classical
    "http://www.youtube.com/watch?v=ipzR9bhei_o" # Bach, Toccata and Fugue in D minor, organ

])

curr_video = seed_videos.random()

for i in range(0,4):
    
    display(text=curr_video.title(),duration=2)
    display(text=curr_video.description(),duration=2)
    
    clip_duration = 1

    video_duration = curr_video.duration()
    clip_offset = random.uniform(0, video_duration-clip_duration)

    videoplayer.play(video=curr_video,offset=clip_offset,duration=clip_duration)
    
    user_liked_song = ask_yes_no("Did you like that song?")

    if user_liked_song == True:
        curr_video = curr_video.related()
    else:
        curr_video = seed_videos.random()