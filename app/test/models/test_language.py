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
            title = TextValue("Show video title"),
            comment = TextValue(""),
            duration = NumberValue(2),
            text = YoutubeVideoGetTitleOperation(curr_video)
        )

        scene2 = TextScene(
            title = TextValue("Show video description"),
            comment = TextValue(""),
            duration = NumberValue(2),
            text = YoutubeVideoGetDescriptionOperation(curr_video)
        )

        clip_duration = NumberValue(1)
        video_duration = YoutubeVideoGetDurationOperation(curr_video)
        clip_offset = GetRandomNumberBetweenIntervalOperation(
            NumberValue(0), SubtractOperation(video_duration,clip_duration)
        )

        scene3 = VideoScene(
            title = TextValue("Play video"),
            comment = TextValue(""),
            duration = clip_duration,
            offset = clip_offset,
            source = curr_video
        )

if __name__ == "__main__":
    unittest.main()