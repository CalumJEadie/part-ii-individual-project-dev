# -*- coding: utf-8 -*-

"""
YouTube API.

Implemented using YouTube Data API.

References:
- https://developers.google.com/youtube/1.0/developers_guide_python#UnderstandingVideos.
"""

import logging
import collections
import re
import random

import gdata.youtube
import gdata.youtube.service

from show import show

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Initialising YouTubeService object")
yt_service = gdata.youtube.service.YouTubeService()

def extract_video_id(url):
    """
    Extracts video identifier from web url.

    >>> extract_video_id("http://www.youtube.com/watch?v=9bZkp7q19f0&feature=g-all-f&context=G27f364eFAAAAAAAAAAA")
    '9bZkp7q19f0'
    >>> extract_video_id("http://www.youtube.com/watch?feature=g-all-f&v=9bZkp7q19f0&context=G27f364eFAAAAAAAAAAA")
    '9bZkp7q19f0'
    >>> extract_video_id('<iframe width="560" height="315" src="http://www.youtube.com/embed/9bZkp7q19f0" frameborder="0" allowfullscreen></iframe>')
    '9bZkp7q19f0'
    >>> extract_video_id("youtube.com/v/9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id("youtube.com/vi/9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id("youtube.com/?v=9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id("youtube.com/?vi=9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id("youtube.com/watch?v=9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id("youtube.com/watch?vi=9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id("youtu.be/9bZkp7q19f0")
    '9bZkp7q19f0'

    >>> extract_video_id("http://vimeo.com/48100473")
    Traceback (most recent call last):
        ...
    VideoIdentifierError: http://vimeo.com/48100473
    """

    # Based on http://rubular.com/r/M9PJYcQxRW / http://stackoverflow.com/questions/3392993/php-regex-to-get-youtube-video-id
    video_id_re = '(?<=(?:v|i)=)[a-zA-Z0-9-]+(?=&)|(?<=(?:v|i)\/)[^&\n]+|(?<=embed\/)[^"&\n]+|(?<=(?:v|i)=)[^&\n]+|(?<=youtu.be\/)[^&\n]+'
    matches = re.search(video_id_re,url)
    if matches is None:
        raise VideoIdentifierError(url)
    return matches.group(0)

class VideoIdentifierError(Exception):
    """
    Exception raised when a video identifier does not correspond to a
    publically accessible video.
    """
    pass

class Video:
    """
    Representation of a particular video.
    """

    def __init__(self,entry):
        """
        Constructs a Video object from a YouTubeVideoEntry object.

        :type entry: gdata.youtube.YouTubeVideoEntry
        :rtype: Video
        """
        self._entry = entry

    @classmethod
    def from_web_url(cls,url):
        """
        Constructs a Video object from a web url.
        """
        video_id = extract_video_id(url)
        entry = yt_service.GetYouTubeVideoEntry(video_id=video_id)
        return cls(entry)

    def __str__(self):
        return "Video(title=%s,duration=%s)" % (self.title(),self.duration())

    def title(self):
        return self._entry.media.title.text

    def description(self):
        return self._entry.media.description.text

    def duration(self):
        return int(self._entry.media.duration.seconds)

    def related(self):
        """
        rtype: VideoCollection
        """
        show(self._entry.id.text)
        #related_feed = yt_service.GetYouTubeRelatedVideoFeed(uri=self._entry.id.text)
        related_feed = yt_service.GetYouTubeRelatedVideoFeed(video_id="9bZkp7q19f0")
        show(related_feed)
        return VideoCollection.from_feed(related_feed)

class VideoCollection(collections.Sequence):
    """
    An ordered collection of videos.

    This could be implemented by subclassing list however at this point not clear
    what the interface to VideoCollection should be. Will use delegation-composition
    and selectively build interface.
    """

    def __init__(self,videos=[]):
        """
        :param videos: YouTube video web urls
        :type videos: String iterable
        """
        self._videos = map(Video.from_web_url,videos)

    @classmethod
    def from_feed(cls,feed):
        """
        Constructs a VideoCollection object from a YouTubeVideoFeed object.

        :type feed: gdata.youtube.YouTubeVideoFeed
        :rtype: VideoCollection
        """
        videos = []
        for entry in feed.entry:
            videos.append(Video(entry))
        return cls(videos)

    def __getitem__(self,key):
        return self._videos.__getitem__(key)

    def __len__(self):
        return self._videos.__len__()

    def random(self):
        """
        Return a random video from this collection.

        :rtype: Video
        """
        return random.choice(self._videos)