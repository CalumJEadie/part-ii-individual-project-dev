"""
Integration tests for the APIs.

Motivating applications are used to shape development of the APIs.

Motivating applications:

1.  Smart music player - plays related songs or switchs to different types of
    music depending on user interaction.
"""

import unittest
import random
import logging
import logging.config

from app.api.core import display,ask_yes_no
from app.api import youtube,videoplayer

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class SmartMusicPlayer(unittest.TestCase):

    def test(self):

        # Task: Start with a seed video.
        # 
        # Implementation options:
        # 
        # 1. Predefined set of possible seed videos.
        # 2. Result of a search using a predefined set of seed keywords.
        # 
        # To get the player off to a good start and make sure it is a music video
        # that's played will go for (1).
        
        # Task: Define a set of seed videos.
        # 
        # How should a video be identified?
        # 
        # Important to consider what a user of YouTube is exposed to.
        # - YouTube urls eg. http://www.youtube.com/watch?v=9bZkp7q19f0
        # - Video titles eg. PSY - GANGNAM STYLE
        # - Video thumbnails
        # - Video hashs eg. 9bZkp7q19f0
        # 
        # YouTube urls have desirable properties that they are unique and it's
        # obvious what they correspond to. Therefore YouTube urls will be used to
        # identify videos.
        # 
        # How should the collection of videos be represented?
        # 
        # Collection will need order, for example as may want to sort on popularity
        # or date added. This motivates use of a list.
        # 
        # Idea of a list may not be suffeciently flexible. This motivates using
        # the more general notion of a collection. Will review.

        # Update: Using from_web_urls for clarity in API.

        seed_videos = youtube.VideoCollection.from_web_urls([
            # Generated using YouTube Music Top Tracks.
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
            # Adding some more genres to make it more interesting!
            # Metal
            "http://www.youtube.com/watch?v=v_09wFxoaeQ", # Slipknot - Before I Forget
            # Classical
            "http://www.youtube.com/watch?v=ipzR9bhei_o" # Bach, Toccata and Fugue in D minor, organ

        ])

        # Task: Randomly select a seed video from the collection of seed videos.

        curr_video = seed_videos.random()

        # Task: Main loop of the program. Play a section of the video. Ask for user
        # feedback and either play a section of a related video or use a new seed.

        for i in range(0,4):

            # Task: Show video title and description.
            # 
            # Need an API for displaying text. Later will need to accept
            # inputs as well. Add these features as if they were language features
            # like print and raw_input.
            
            display(text=curr_video.title(),duration=5)
            display(text=curr_video.description(),duration=5)

            # Task: Play section of currently selected video.
            #
            # Want to keep user engaged and as music videos often start slowly
            # will play clip at random offset into the video.
            # 
            # Should random.uniform be used at expense of understanding what
            # the line does or should a more descriptive method like
            # generateRandomNumberWithinInterval which would teach users less
            # about specific Python language features?
            
            clip_duration = 10

            video_duration = curr_video.duration()
            clip_offset = random.uniform(0, video_duration-clip_duration)

            # How should the video playing API be referenced?
            # 
            # May want to consider treating the Video playing API likes the CPU
            # YouTube API like main memory. This analogy be be confusing however.
            # 
            # More educational content is using more conventional module names.
            # 
            # To allow the API to use different video playing applications
            # in the background don't want to reference particular applications.
            # May want to consider how could intergrate OpenGL capabilities however
            # will defer this as unlikely to be relevant.
            # 
            # Using named arguments makes it clearer what's going on.
            # Less **hidden dependancies**.

            videoplayer.play(video=curr_video,offset=clip_offset,duration=clip_duration)

            # Task: Get user feedback.
            # 
            # Implement as basic language feature, like print and raw_input.
            
            user_liked_song = ask_yes_no("Did you like that song?")

            # Task: Choose a related song or a new seed depending on whether
            # user liked the previous one.
            # 
            # Being explicit in comparing to True makes it clearer to the user
            # what the language is doing. This remove hidden dependance and 
            # increases role expressiveness.

            if user_liked_song == True:

                # Task: Choose a related video.
                # 
                # There will be very many related videos.
                # How should the related video be selected?
                # Should selection process be exposed or left to the API to
                # implement.

                curr_video = curr_video.related().random()

            else:

                curr_video = seed_videos.random()

if __name__ == "__main__":
    unittest.main()
