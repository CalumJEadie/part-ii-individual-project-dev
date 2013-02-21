"""
Examples.

Trying to increase complexity incrementally with vue to use examples within evaluation.

General principles:
- Increasing complexity
- Prefer smaller jumps
- Prefer strongly motivational examples
- Prefer familiar concepts first, like search before related
- Prefer examples where motivation to use features is strong.
"""

from app.models.language import *
from app.api.videoplayer import Speed

# Important to have interesting examples to keep users interested.
# Have used popularity, in particular view, to create a list of "interesting" videos.
# Have also added some personal interest ones!

# http://news.sky.com/story/1027734/youtubes-top-10-videos-of-2012-revealed

GANGNAM_STYLE = "http://www.youtube.com/watch?v=9bZkp7q19f0"
# Somebody That I Used to Know - Walk off the Earth (Gotye - Cover)
SOMEBODY = "http://www.youtube.com/watch?v=d9NF2edxy-M"
# "Call Me Maybe" by Carly Rae Jepsen - Feat. Justin Bieber, Selena, Ash
CALL_ME_MAYBE = "http://www.youtube.com/watch?v=AsBsBU3vn6M"
# A DRAMATIC SURPRISE ON A QUIET SQUARE
SURPRISE = "http://www.youtube.com/watch?v=316AzLYfAzw"
# Dubstep Violin Original- Lindsey Stirling- Crystallize
DUBSTEP_VIOLIN = "http://www.youtube.com/watch?v=aHjpOzsQ9YI"
# Felix Baumgartner's supersonic freefall from 128k' - Mission Highlights
FREEFALL = "http://www.youtube.com/watch?v=FHtvDA0W34I"

# YouTube Interactive Timeline

# Isaac's Live Lip-Dub Proposal
PROPOSAL = "http://www.youtube.com/watch?v=DTCmHC8IuuI"
# San Diego Fireworks 2012, LOUD and up close
FIREWORKS = "http://www.youtube.com/watch?v=ndVhgq1yHdA"

# Others

# David Guetta - She Wolf (Lyrics Video) ft. Sia
SHE_WOLF = "http://www.youtube.com/watch?v=uweWiCLT8Eg"
# THE BEARDS - If Your Dad Doesn't Have a Beard, You've Got Two Mums
YOUVE_GOT_TWO_MUMS = "http://www.youtube.com/watch?v=RmFnarFSj_U"
# A Pep Talk from Kid President to You
PEP_TALK = "http://www.youtube.com/watch?v=l-gQLqv9f4o"
# World's Largest Rope Swing
ROPE_SWING = "http://www.youtube.com/watch?v=4B36Lr0Unp4"
# Danny MacAskill - "Way Back Home"
MAC_ASKILL = "http://www.youtube.com/watch?v=Cj6ho1-G6tw"

acts = [

    # Introduce: Video
    
    Act(
        "A single video",
        [
            VideoScene(
                "Play Gangnam style for 5 seconds from offset of 0 seconds.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                VideoValue(GANGNAM_STYLE) 
        )
        ]
    ),

    # TODO: Introduce volume.
    # Explanation: I like to listen to my music loud!
    
    Act(
        "Volume",
        [
            VideoScene(
                "Play Gangnam style for 10 seconds from offset of 0 seconds with volume 50 dB.",
                "",
                NumberValue(10),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                VideoValue(GANGNAM_STYLE),
                NumberValue(50)
            )
        ]
    ),
    
    # TODO: Introduce speed.
    # Explanation: I really like this video but it takes a while to get going, I
    # want to play through it quickly.
    
    Act(
        "Speed",
        [
            VideoScene(
                "Play A DRAMATIC SURPRISE ON A QUIET SQUARE very fast.",
                "",
                NumberValue(10),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                VideoValue(SURPRISE),
                NumberValue(0),
                SpeedValue(Speed.VFast)
            )
        ]
    ),

    # Introduce: Offset.
    # Explanation: The introduction to Felix Baumgartner's supersonic freefall is really slow,
    # I want to skip it.
    
    Act(
        "Offset",
        [
            VideoScene(
                "Skip to the best bit of Felix Baumgartner's supersonic freefall",
                "",
                NumberValue(10),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(60),
                VideoValue(FREEFALL) 
        )
        ]
    ),

    # Introduce video collections and search.
    # Explanation: I want to play a science festival video.

    Act(
        "Searching YouTube",
        [
            VideoScene(
                "Search YouTube for Science Festival videos and play one.",
                "",
                NumberValue(10),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                YoutubeVideoCollectionRandom(
                    YoutubeSearch(
                        TextValue("cambridge science festival")
                    )
                ) 
        )
        ]
    ),

    # Introduce: Related videos
    # Explanation: I really like Kid President, so I want to find videos related
    # to Pep Talk

    Act(
        "Related videos",
        [
            VideoScene(
                "Play a video related to Kid President's Pep Talk",
                "",
                NumberValue(10),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                YoutubeVideoCollectionRandom(
                    YoutubeVideoGetRelated(
                        VideoValue(PEP_TALK) 
                    )
                )
            )
        ]
    ),

    # Introduce: Scenes
    # Explanation: I really like the World Large Rope Swing video and adventure sports
    # I'd like to several bits from those videos
    
    Act(
        "Scenes",
        [
            VideoScene(
                "Play Worlds Largest Rope Swing video.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                VideoValue(ROPE_SWING)
            ),
            VideoScene(
                "Play video related to the Worlds Largest Rope Swing video.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                YoutubeVideoCollectionRandom(
                    YoutubeVideoGetRelated(
                        VideoValue(ROPE_SWING) 
                    )
                )
            ),
            VideoScene(
                "Play another video related to the Worlds Largest Rope Swing video.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                YoutubeVideoCollectionRandom(
                    YoutubeVideoGetRelated(
                        VideoValue(ROPE_SWING) 
                    )
                )
            )
        ]
    ),

    # Introduce: Arithmetic
    # Explanation: I like the adventure sports videos but want to get straight into the action.
    
    # TODO: add get duration and random
    # TODO: play from random parts of video

    # Act(
    #     "Scenes",
    #     [
    #         VideoScene(
    #             "Play Worlds Largest Rope Swing video.",
    #             "",
    #             NumberValue(5),
    #             CommandSequence([]),
    #             CommandSequence([]),
    #             NumberValue(0),
    #             VideoValue(ROPE_SWING)
    #         ),
    #         VideoScene(
    #             "Play video related to the Worlds Largest Rope Swing video.",
    #             "",
    #             NumberValue(5),
    #             CommandSequence([]),
    #             CommandSequence([]),
    #             NumberValue(0),
    #             YoutubeVideoGetRelated(
    #                 VideoValue(ROPE_SWING) 
    #             )
    #         ),
    #         VideoScene(
    #             "Play another video related to the Worlds Largest Rope Swing video.",
    #             "",
    #             NumberValue(5),
    #             CommandSequence([]),
    #             CommandSequence([]),
    #             NumberValue(0),
    #             YoutubeVideoGetRelated(
    #                 VideoValue(ROPE_SWING) 
    #             )
    #         )
    #     ]
    # ),

    
    # Introduce: Text scene, title and comments
    # Explanation: I like mountain biking videos. I like to know what I'm watching and what
    # other people are saying about it.
    
    Act(
        "Titles and comments",
        [
            TextScene(
                "Display title of Danny MacAskill's - Way Back Home video.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                YoutubeVideoGetTitle(VideoValue(MAC_ASKILL))
            ),
            VideoScene(
                "Play some of Danny MacAskill's - Way Back Home video.",
                "",
                NumberValue(10),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(90),
                VideoValue(MAC_ASKILL)
            ),
            TextScene(
                "Display a comment from Danny MacAskill's - Way Back Home video.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                YoutubeVideoRandomComment(VideoValue(MAC_ASKILL))
            ),
            TextScene(
                "Display another comment from Danny MacAskill's - Way Back Home video.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                YoutubeVideoRandomComment(VideoValue(MAC_ASKILL))
            ),
            TextScene(
                "Display another comment from Danny MacAskill's - Way Back Home video.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                YoutubeVideoRandomComment(VideoValue(MAC_ASKILL))
            ),
            VideoScene(
                "Play some more of Danny MacAskill's - Way Back Home video.",
                "",
                NumberValue(10),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(110),
                VideoValue(MAC_ASKILL)
            ),
        ]
    ),





    Act(
        "",
        [
            VideoScene(
                "Play Gangnam style for 5 seconds from offset of 0 seconds.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(60),
                VideoValue(GANGNAM_STYLE) 
        )
        ]
    ),
    Act(
        "",
        [
            TextScene(
                "Displays the title of a video, click `perform` to find out what it it!",
                "",
                NumberValue(2),
                CommandSequence([]),
                CommandSequence([]),
                YoutubeVideoGetTitle(VideoValue("http://www.youtube.com/watch?v=uweWiCLT8Eg")) # David Guetta - She Wolf (Lyrics Video) ft. Sia
            ),
            VideoScene(
                "Plays the video.",
                "",
                NumberValue(2),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                VideoValue("http://www.youtube.com/watch?v=uweWiCLT8Eg") # David Guetta - She Wolf (Lyrics Video) ft. Sia
            )
    ]),
    Act(
        "",
        [
            TextScene(
                "Use this space to write about a scene, this one displays the title of Gangnam Style.",
                "The Gangnam Style video is identified by it's web page and saved for later in the variable `curr video`.",
                NumberValue(2),
                CommandSequence([
                    VideoSetVariableStatement(
                        "curr video",
                        VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
                    )
                ]),
                CommandSequence([]),
                YoutubeVideoGetTitle(VideoGetVariableExpression("curr video"))
            ),
            VideoScene(
                "This scene plays Gangnam Style.",
                "We get hold of the video by using the variable we stored it in earlier.",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                VideoGetVariableExpression("curr video")
            ),
            TextScene(
                "Display title of a related video.",
                "We select a random related video and use that from now on.",
                NumberValue(2),
                CommandSequence([
                    VideoSetVariableStatement(
                        "curr video",
                        YoutubeVideoCollectionRandom(
                            YoutubeVideoGetRelated(
                                VideoGetVariableExpression("curr video")
                            )
                        )
                    )
                ]),
                CommandSequence([]),
                YoutubeVideoGetTitle(VideoGetVariableExpression("curr video"))
            ),
            VideoScene(
                "This scene plays the related video.",
                "",
                NumberValue(5),
                CommandSequence([]),
                CommandSequence([]),
                NumberValue(0),
                VideoGetVariableExpression("curr video")
            )
    ])
]