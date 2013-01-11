"""
Unit tests for language models.
"""

import unittest
import logging

from app.models.language import *
from app.test import motivating_applications

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

    @unittest.skip
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

    def test_language_component_children(self):
        """
        Tests to get to the bottom and check for unusual _children
        behaviour.

        Behavior isolated - needed to turn _children from a class variable
        to an instance variable.
        """

        self.assertEqual(
            NumberValue(1)._children,
            []
        )

        self.assertEqual(
            TextValue("one")._children,
            []
        )

        a = NumberValue(2)
        b = NumberValue(3)
        self.assertEqual(
            Add(a,b)._children,
            [a,b]
        )

    @unittest.skip
    def test_get_live_variables(self):

        self.assertEqual(
            GetVariableExpression("a").get_live_variables(),
            set(["a"])
        )

        self.assertEqual(
            TextValue("one").get_live_variables(),
            set([])
        )

        # self.assertEqual(
        #     NumberValue(1).get_live_variables(),
        #     set([])
        # )

        # self.assertEqual(
        #     SetVariableStatement("a",NumberValue(1)).get_live_variables(),
        #     set()
        # )

        # self.assertEqual(
        #     CommandSequence([
        #         SetVariableStatement("a",NumberValue(1)),
        #         SetVariableStatement("b",TextValue("one")),
        #         SetVariableStatement("c",
        #             Add(
        #                 GetVariableExpression("a"),
        #                 GetVariableExpression("b")
        #             )
        #         )
        #     ]).get_live_variables(),
        #     set(["a","b","c"])
        # )      

        # VideoScene(
        #         title = "Play video",
        #         comment = "",
        #         duration = GetVariableExpression("clip_duration"),
        #         pre_commands = CommandSequence([
        #             SetVariableStatement("clip_duration", NumberValue(1)),
        #             SetVariableStatement("video_duration", YoutubeVideoGetDuration(curr_video)),
        #             SetVariableStatement("clip_offset",
        #                 GetRandomNumberBetweenInterval(
        #                     NumberValue(0),
        #                     Subtract(
        #                         GetVariableExpression("video_duration"),
        #                         GetVariableExpression("clip_duration")
        #                     )
        #                 )
        #             )
        #         ]),
        #         post_commands = CommandSequence([]),
        #         offset = GetVariableExpression("clip_offset"),
        #         source = GetVariableExpression("curr_video")
        #     )  
        
        # motivating_applications.smart_music_player.get_live_variables()

if __name__ == "__main__":
    unittest.main()