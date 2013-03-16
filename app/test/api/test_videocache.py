"""
Unit tests for Video caching API.

The cache will be engineering around constraints tested in these tests.

timeit repeats calculations very many times so is not suitable. However, will use
it's utility methods for accuracy and portability.
"""

import unittest
import logging
import itertools
import os
import timeit
import random
import time

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from app.api import videocache
from app.api.youtube import *

# Constraints. Make sure cache meets it's guarantees.
# Seconds are used as resolution is suffcient and difficult to get better accuracy in timing.
MAX_NOT_CACHED_GET_TIME = videocache.MAX_NOT_CACHED_GET_TIME
MAX_CACHED_GET_TIME = videocache.MAX_CACHED_GET_TIME
MIN_VIDEO_READY_FILE_SIZE = videocache.MIN_VIDEO_READY_FILE_SIZE

# Test data - YouTube Music Top 30 Tracks - 08/02/2013
# http://www.youtube.com/music
VIDEOS = [Video.from_web_url("http://www.youtube.com/watch?v=QK8mJJJvaes"),
    Video.from_web_url("http://www.youtube.com/watch?v=9bZkp7q19f0"),
    #Video.from_web_url("http://www.youtube.com/watch?v=HsfY8iFbYjE"), private
    Video.from_web_url("http://www.youtube.com/watch?v=vNoKguSdy4Y"),
    Video.from_web_url("http://www.youtube.com/watch?v=T4cdfRohhcg"),
    Video.from_web_url("http://www.youtube.com/watch?v=kYtGl1dX5qI"),
    Video.from_web_url("http://www.youtube.com/watch?v=OpQFFLBMEPI"),
    Video.from_web_url("http://www.youtube.com/watch?v=ifRoMGG8Wvs"),
    Video.from_web_url("http://www.youtube.com/watch?v=D1gl46hh3sQ"),
    Video.from_web_url("http://www.youtube.com/watch?v=lWA2pjMjpBs"),
    #Video.from_web_url("http://www.youtube.com/watch?v=JHDbvMtMsbg"), private
    # Removing for performance
    # Video.from_web_url("http://www.youtube.com/watch?v=Ys7-6_t7OEQ"),
    # Video.from_web_url("http://www.youtube.com/watch?v=bek1y2uiQGA"),
    # Video.from_web_url("http://www.youtube.com/watch?v=xGPeNN9S0Fg"),
    # Video.from_web_url("http://www.youtube.com/watch?v=cN4fNaUAMbA"),
    # Video.from_web_url("http://www.youtube.com/watch?v=CqPU7NSVQwY"),
    # Video.from_web_url("http://www.youtube.com/watch?v=e-fA-gBCkj0"),
    # Video.from_web_url("http://www.youtube.com/watch?v=FOjdXSrtUxA"),
    # Video.from_web_url("http://www.youtube.com/watch?v=bqIxCtEveG8"),
    # Video.from_web_url("http://www.youtube.com/watch?v=-6YLi0GNBTk"),
    # Video.from_web_url("http://www.youtube.com/watch?v=F90Cw4l-8NY"),
    # Video.from_web_url("http://www.youtube.com/watch?v=WA4iX5D9Z64"),
    # Video.from_web_url("http://www.youtube.com/watch?v=cOQDsmEqVt8"),
    # Video.from_web_url("http://www.youtube.com/watch?v=G_miGclPFGs"),
    # Video.from_web_url("http://www.youtube.com/watch?v=4aQDOUbErNg"),
    # Video.from_web_url("http://www.youtube.com/watch?v=1y6smkh6c-0"),
    # Video.from_web_url("http://www.youtube.com/watch?v=fwK7ggA3-bU"),
    # Video.from_web_url("http://www.youtube.com/watch?v=dPKG1-3LXBs"),
    # Video.from_web_url("http://www.youtube.com/watch?v=R4em3LKQCAQ"),
    #Video.from_web_url("http://www.youtube.com/watch?v=7iHd6uOGqII") UMG
]

# def get_cache_contents():
#     contents = []
#     for location in videocache.LOCATIONS:
#         contents.extend(map(lambda f: os.path.join(location, f), os.listdir(location)))
#     return contents

class AssertionMixin(object):
    """
    Adds additional assertions to unit test to make tests clearer.
    """

    def assertVideoReady(self, path):
        """
        Test that the video at path is ready to be played.

        Assumes that will be played from the beginning.    

        :type self: unittest.TestCase
        """
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(os.access(path, os.R_OK))
        self.assertGreater(os.path.getsize(path), MIN_VIDEO_READY_FILE_SIZE)

    def assertOkNotCachedGetTime(self, t0, t1):
        t = t1 - t0
        self.assertLess(t, MAX_NOT_CACHED_GET_TIME)

    def assertOkCachedGetTime(self, t0, t1):
        t = t1 - t0
        self.assertLess(t, MAX_CACHED_GET_TIME)

class Test(unittest.TestCase, AssertionMixin):

    def test_clear(self):
        videocache.init()
        videocache.clear()

    def test_get_performance(self):
        videocache.init()
        videocache.clear()

        # Test data.
        # Randomly choose subset of videos.
        videos_sample = random.sample(VIDEOS, 5)

        # Test not cached time.
        for video in videos_sample:
            t0 = timeit.default_timer()
            video_path = videocache.get(video)
            t1 = timeit.default_timer()
            self.assertVideoReady(video_path)
            self.assertOkNotCachedGetTime(t0, t1)

            # Offset downloads.
            time.sleep(2)

        # Test cached time.
        for video in videos_sample:
            t0 = timeit.default_timer()
            video_path = videocache.get(video)
            t1 = timeit.default_timer()
            self.assertVideoReady(video_path)
            self.assertOkCachedGetTime(t0, t1)

            # Offset downloads.
            time.sleep(2)

class TestPreload(unittest.TestCase):

    def test_preload(self):

        import app.api.youtube
        from app.models import examples

        videocache.init()

        # Every video value that occurs in an example or the editor interface.
        seed_videos_urls = [
            examples.GANGNAM_STYLE,
            examples.SURPRISE,
            examples.FREEFALL,
            examples.PEP_TALK,
            examples.ROPE_SWING,
            examples.FIREWORKS,
            examples.MAC_ASKILL,
            examples.CAMBRIDGE_HARLEM
        ]
        seed_videos = map(Video.from_web_url, seed_videos_urls)

        # Derive set of videos likely to be returned by related to.
        related_videos = set()
        for seed_video in seed_videos:
            related_videos |= set(seed_video.related())

        videocache.prime(seed_videos)
        videocache.prime(related_videos)

if __name__ == "__main__":
    unittest.main()
