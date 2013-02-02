"""
Unit tests for YouTube API.
"""

import unittest
import logging
import doctest

from app.api import youtube

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TestDoctests(unittest.TestCase):

    def test_doctests(self):
        doctest.testmod(youtube)

class TestVideoGangnam(unittest.TestCase):
    """
    Unit tests for the Video class.

    Use Gangnam Style as it's the current most popular video and so
    it's unlikely that it'll be removed.
    """

    def test_title(self):
        gangnam_style_url = "http://www.youtube.com/watch?v=9bZkp7q19f0"
        video = youtube.Video.from_web_url(gangnam_style_url)
        self.assertIn("psy - gangnam",video.title().lower())

    def test_description(self):
        gangnam_style_url = "http://www.youtube.com/watch?v=9bZkp7q19f0"
        video = youtube.Video.from_web_url(gangnam_style_url)
        self.assertIn("http://www.facebook.com/officialpsy",video.description().lower())

    def test_duration(self):
        gangnam_style_url = "http://www.youtube.com/watch?v=9bZkp7q19f0"
        video = youtube.Video.from_web_url(gangnam_style_url)
        duration = 4*60 + 13
        self.assertGreater(video.duration(),duration-2)
        self.assertLess(video.duration(),duration+2)

    def test_related(self):
        gangnam_style_url = "http://www.youtube.com/watch?v=9bZkp7q19f0"
        video = youtube.Video.from_web_url(gangnam_style_url)
        related = video.related()
        self.assertGreater(len(related),5)

    def test_random_comment(self):
        gangnam_style_url = "http://www.youtube.com/watch?v=9bZkp7q19f0"
        video = youtube.Video.from_web_url(gangnam_style_url)

        comment1 = video.random_comment()
        comment2 = video.random_comment()
        comment3 = video.random_comment()

        self.assertNotEqual(comment1, comment2) # Expect them to be different, may fail.
        self.assertNotEqual(comment2, comment3) # Expect them to be different, may fail.

class TestVideoCollection(unittest.TestCase):
    """
    Unit tests for the VideoCollection class.

    Use popular music tracks as unlikely to be removed.
    """

    urls = [
        "http://www.youtube.com/watch?v=9bZkp7q19f0", # PSY - GANGNAM STYLE
        "http://www.youtube.com/watch?v=lJqbaGloVxg", # James Arthur - Impossible - Official Single
        "http://www.youtube.com/watch?v=kYtGl1dX5qI", # will.i.am - Scream & Shout ft. Britney Spears
        "http://www.youtube.com/watch?v=bqIxCtEveG8", # Labrinth feat. Emeli Sande - Beneath Your Beautiful
        "http://www.youtube.com/watch?v=KHF9itPLUo4" # Johnny Cash - I Walk the Line
    ]

    def test_from_web_urls(self):
        videos = youtube.VideoCollection.from_web_urls(self.urls)

    def test_len(self):
        videos = youtube.VideoCollection.from_web_urls(self.urls)
        self.assertEqual(len(videos),len(self.urls))

class Test(unittest.TestCase):
    """
    Unit tests for module levels methods.
    """

    def test_search(self):
        videos = youtube.search("music")
        self.assertGreater(len(videos), 0)

    def test_top_rated(self):
        videos = youtube.top_rated()
        self.assertGreater(len(videos), 0)

    def test_most_viewed(self):
        videos = youtube.most_viewed()
        self.assertGreater(len(videos), 0)

    def test_recently_featured(self):
        videos = youtube.recently_featured()
        self.assertGreater(len(videos), 0)

    def test_most_recent(self):
        videos = youtube.most_recent()
        self.assertGreater(len(videos), 0)

if __name__ == "__main__":
    unittest.main()
