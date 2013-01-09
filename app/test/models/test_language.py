"""
Unit tests for language models.
"""

import unittest
import logging

from app.models.language import *

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class SmartMusicPlayerTest(unittest.TestCase):
    """
    Uses Smart Music Player motivating application.
    """

    def test_create_act(self):
        """
        Tests creating act to describe motivating application.
        """
        pass

    def test_create_inner_loop_scenes(self):
        """
        Tests creating scenes to describe inner loop from the example.
        """

        curr_video = VideoExpression()

        scene1 = TextScene(
            title = "Show video title",
            comment = "",
            duration = NumberValue(2),
            text = YoutubeVideoGetTitle(curr_video)
        )

        scene2 = TextScene(
            title = "Show video description",
            comment = "",
            duration = NumberValue(2),
            text = YoutubeVideoGetDescription(curr_video)
        )

        scene3 = VideoScene(
            title = "Play video",
            comment = "",
            duration = GetVariableExpression("clip_duration"),
            pre_commands = CommandSequence([
                SetVariableStatement("clip_duration", NumberValue(1)),
                SetVariableStatement("video_duration", YoutubeVideoGetDuration(curr_video)),
                SetVariableStatement("clip_offset",
                    GetRandomNumberBetweenInterval(
                        NumberValue(0),
                        Subtract(
                            GetVariableExpression("video_duration"),
                            GetVariableExpression("clip_duration")
                        )
                    )
                )
            ]),
            post_commands = CommandSequence([]),
            offset = GetVariableExpression("clip_offset"),
            source = GetVariableExpression("curr_video")
        )

    def test_translate_inner_loop_scenes(self):
        """
        Tests translating scenes describing inner loop from the example.
        """

        curr_video = VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0") # PSY - GANGNAM STYLE

        act1 = Act([

            TextScene(
                title = "Show video title",
                comment = "",
                duration = NumberValue(2),
                text = YoutubeVideoGetTitle(curr_video)
            ),

            TextScene(
                title = "Show video description",
                comment = "",
                duration = NumberValue(2),
                text = YoutubeVideoGetDescription(curr_video)
            ),

            VideoScene(
                title = "Play video",
                comment = "",
                duration = GetVariableExpression("clip_duration"),
                pre_commands = CommandSequence([
                    SetVariableStatement("clip_duration", NumberValue(1)),
                    SetVariableStatement("video_duration", YoutubeVideoGetDuration(curr_video)),
                    SetVariableStatement("clip_offset",
                        GetRandomNumberBetweenInterval(
                            NumberValue(0),
                            Subtract(
                                GetVariableExpression("video_duration"),
                                GetVariableExpression("clip_duration")
                            )
                        )
                    )
                ]),
                post_commands = CommandSequence([]),
                offset = GetVariableExpression("clip_offset"),
                source = GetVariableExpression("curr_video")
            )

        ])

        print act1.translate()

    def test_operators(self):
        """
        Tests of representation of standard Python operators.
        """
        exec Add(NumberValue(1),NumberValue(2)).translate()
        exec Subtract(NumberValue(1),NumberValue(2)).translate()
        exec Multiply(NumberValue(1),NumberValue(2)).translate()

    def test_instance_methods(self):
        """
        Tests of representation of instance methods.
        """
        InstanceMethod0(
            VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0"),
            "title"
        ).translate()

        YoutubeVideoGetTitle(
            VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
        ).translate()

        InstanceMethod0(
            VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0"),
            "description"
        ).translate()

        YoutubeVideoGetDescription(
            VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
        ).translate()

if __name__ == "__main__":
    unittest.main()