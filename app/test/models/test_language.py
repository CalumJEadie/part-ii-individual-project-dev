"""
Unit tests for language models.
"""

import unittest
import logging
import doctest

from app.models.language import *
from app.test import motivating_applications

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TestDoctests(unittest.TestCase):

    def test_doctests(self):
        doctest.testmod(app.models.language)

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
            text = YoutubeVideoGetTitle(curr_video),
            pre_commands = CommandSequence([]),
            post_commands = CommandSequence([])
        )

        scene2 = TextScene(
            title = "Show video description",
            comment = "",
            duration = NumberValue(2),
            text = YoutubeVideoGetDescription(curr_video),
            pre_commands = CommandSequence([]),
            post_commands = CommandSequence([])
        )

        scene3 = VideoScene(
            title = "Play video",
            comment = "",
            duration = NumberGetVariableExpression("clip_duration"),
            pre_commands = CommandSequence([
                NumberSetVariableStatement("clip_duration", NumberValue(1)),
                NumberSetVariableStatement("video_duration", YoutubeVideoGetDuration(curr_video)),
                NumberSetVariableStatement("clip_offset",
                    GetRandomNumberBetweenInterval(
                        NumberValue(0),
                        Subtract(
                            NumberGetVariableExpression("video_duration"),
                            NumberGetVariableExpression("clip_duration")
                        )
                    )
                )
            ]),
            post_commands = CommandSequence([]),
            offset = NumberGetVariableExpression("clip_offset"),
            source = VideoGetVariableExpression("curr_video")
        )
        
    def test_translate_inner_loop_scenes(self):
        """
        Tests translating scenes describing inner loop from the example.
        """

        curr_video = VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0") # PSY - GANGNAM STYLE

        act1 = Act("",
            [

            TextScene(
                title = "Show video title",
                comment = "",
                duration = NumberValue(2),
                text = YoutubeVideoGetTitle(curr_video),
                pre_commands = CommandSequence([]),
                post_commands = CommandSequence([])
            ),

            TextScene(
                title = "Show video description",
                comment = "",
                duration = NumberValue(2),
                text = YoutubeVideoGetDescription(curr_video),
                pre_commands = CommandSequence([]),
                post_commands = CommandSequence([])
            ),

            VideoScene(
                title = "Play video",
                comment = "",
                duration = NumberGetVariableExpression("clip_duration"),
                pre_commands = CommandSequence([
                    NumberSetVariableStatement("clip_duration", NumberValue(1)),
                    NumberSetVariableStatement("video_duration", YoutubeVideoGetDuration(curr_video)),
                    NumberSetVariableStatement("clip_offset",
                        GetRandomNumberBetweenInterval(
                            NumberValue(0),
                            Subtract(
                                NumberGetVariableExpression("video_duration"),
                                NumberGetVariableExpression("clip_duration")
                            )
                        )
                    )
                ]),
                post_commands = CommandSequence([]),
                offset = NumberGetVariableExpression("clip_offset"),
                source = VideoGetVariableExpression("curr_video")
            )

        ])
        # print act1.translate()

class Test(unittest.TestCase):
    """
    General tests.
    """

    def test_operator_functions(self):

        exec translate_operator_2("+",NumberValue(1),NumberValue(1))
        exec translate_operator_2("-",NumberValue(1),NumberValue(1))

    def test_operators(self):
        """
        Tests of representation of standard Python operators.
        """
        exec Add(NumberValue(1),NumberValue(2)).translate()
        exec Add(NumberValue(1),NumberValue(2)).translate()
        exec Subtract(NumberValue(1),NumberValue(2)).translate()
        exec Multiply(NumberValue(1),NumberValue(2)).translate()

    def test_operator_evaluation_order(self):

        # Example where evaluation order different than with brackets.
        # 2 * 3 + 4 -> (2*3) + 4 -> 10
        # 2 * (3 + 4) -> 14
        e = 2 * (3 + 4)
        m = Multiply(
            NumberValue(2),
            Add(
                NumberValue(3),
                NumberValue(4)
            )
        )
        # Can't use eval or exec here, would need more sophisticated methods
        # to check.

    def test_instance_methods(self):
        """
        Tests of representation of instance methods.
        """
        YoutubeVideoGetTitle(
            VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
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

        # Check values have no children.

        self.assertEqual(
            NumberValue(1)._children,
            []
        )

        self.assertEqual(
            TextValue("one")._children,
            []
        )

        self.assertEqual(
            VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")._children,
            []
        )

        self.assertEqual(
            VideoCollectionValue(["http://www.youtube.com/watch?v=9bZkp7q19f0"])._children,
            []
        )

        a = NumberValue(2)
        b = NumberValue(3)
        self.assertEqual(
            Add(a,b)._children,
            [a,b]
        )

    def test_get_live_variables(self):

        self.assertEqual(
            NumberGetVariableExpression("a").get_live_variables(Type.NUMBER),
            set(["a"])
        )

        self.assertEqual(
            TextValue("one").get_live_variables(Type.TEXT),
            set([])
        )

        self.assertEqual(
            NumberValue(1).get_live_variables(Type.NUMBER),
            set([])
        )

        self.assertEqual(
            NumberSetVariableStatement("a",NumberValue(1)).get_live_variables(Type.NUMBER),
            set(["a"])
        )

        
        cs = CommandSequence([
            NumberSetVariableStatement("a", NumberValue(1)),
            NumberSetVariableStatement("b", NumberValue(2)),
            NumberSetVariableStatement("c",
                Add(
                    NumberGetVariableExpression("a"),
                    NumberGetVariableExpression("b")
                )
            ),
            TypedSetVariableStatement(Type.TEXT, "d", TextValue("one")),
            TypedSetVariableStatement(Type.TEXT, "e",
                GetVariableExpression(Type.TEXT, "d")
            )
        ])

        self.assertEqual(
            cs.get_live_variables(Type.NUMBER),
            set(["a","b", "c"])
        )

        self.assertEqual(
            cs.get_live_variables(Type.TEXT),
            set(["d", "e"])
        )

        cs = VideoScene(
            title = "Play video",
            comment = "",
            duration = NumberGetVariableExpression("clip_duration"),
            pre_commands = CommandSequence([
                NumberSetVariableStatement("clip_duration", NumberValue(1)),
                NumberSetVariableStatement("video_duration", YoutubeVideoGetDuration(
                    VideoGetVariableExpression("curr_video")
                )),
                NumberSetVariableStatement("clip_offset",
                    GetRandomNumberBetweenInterval(
                        NumberValue(0),
                        Subtract(
                            NumberGetVariableExpression("video_duration"),
                            NumberGetVariableExpression("clip_duration")
                        )
                    )
                )
            ]),
            post_commands = CommandSequence([]),
            offset = NumberGetVariableExpression("clip_offset"),
            source = VideoGetVariableExpression("curr_video")
        )

        self.assertEqual(
            cs.get_live_variables(Type.NUMBER),
            set(["clip_duration", "video_duration", "clip_offset"])
        )

        self.assertEqual(
            cs.get_live_variables(Type.VIDEO),
            set(["curr_video"])
        )

    def test_indent(self):
        """
        Tests handling of multiple lines and empty lines.
        """

        self.assertEqual(
            indent("""command1
command2

command3"""),"""    command1
    command2

    command3"""
        )

    def test_if_scene(self):

        # Simple if scene
        act = Act("",
            [
            IfScene("Simple If Scene", "",
                TextValue("question?"),
                SceneSequence([
                ]),
                SceneSequence([
                ])
            )
        ])
        # print act.translate()

        # If scene with complex question and scene sequence in both branches.
        curr_video = VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0") # PSY - GANGNAM STYLE

        act = Act("",
            [
            IfScene("Complex If Scene", "",
                GetVariableExpression(Type.TEXT, "question"),
                SceneSequence([
                    TextScene(
                        title = "Show video title",
                        comment = "",
                        duration = NumberValue(2),
                        text = YoutubeVideoGetTitle(curr_video),
                        pre_commands = CommandSequence([]),
                        post_commands = CommandSequence([])
                    )
                ]),
                SceneSequence([
                    TextScene(
                        title = "Show video description",
                        comment = "",
                        duration = NumberValue(2),
                        text = YoutubeVideoGetDescription(curr_video),
                        pre_commands = CommandSequence([]),
                        post_commands = CommandSequence([])
                    )
                ])
            )
        ])
        # print act.translate()

    def test_while_scene(self):

        # Simple while scene
        act = Act("",
            [
            WhileScene("Simple While Scene", "",
                TextValue("question?"),
                SceneSequence([
                ])
            )
        ])
        print act.translate()

        # If scene with complex question and scene sequence in both branches.
        curr_video = VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0") # PSY - GANGNAM STYLE

        act = Act("",
            [
            WhileScene("Complex While Scene", "",
                GetVariableExpression(Type.TEXT, "question"),
                SceneSequence([
                    TextScene(
                        title = "Show video title",
                        comment = "",
                        duration = NumberValue(2),
                        text = YoutubeVideoGetTitle(curr_video),
                        pre_commands = CommandSequence([]),
                        post_commands = CommandSequence([])
                    )
                ])
            )
        ])
        print act.translate()

    def test_variable_name_generator(self):
        """
        Test extreme variable names.
        """

        g = VariableNameGenerator.get_instance()
        g.reset()

        self.assertEqual(
            g.generate(),
            "store_a"
        )

        for i in range(0,24):
            g.generate()

        self.assertEqual(
            g.generate(),
            "store_z"
        )

        self.assertEqual(
            g.generate(),
            "store_aa"
        )

        self.assertEqual(
            g.generate(),
            "store_ab"
        )        

if __name__ == "__main__":
    unittest.main()