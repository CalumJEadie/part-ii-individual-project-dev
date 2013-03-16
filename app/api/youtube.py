# -*- coding: utf-8 -*-

"""
YouTube API.

Implemented using YouTube Data API and youtube-dl.

youtube-dl is used as not obvious how to retrieve streaming urls from Data API.

References:
- https://developers.google.com/youtube/1.0/developers_guide_python#UnderstandingVideos.
"""

import logging
import collections
import re
import random
import subprocess

import gdata.youtube
import gdata.youtube.service

from show import show

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Initialising YouTubeService object")
yt_service = gdata.youtube.service.YouTubeService()

# Based on http://rubular.com/r/M9PJYcQxRW and http://stackoverflow.com/questions/3392993/php-regex-to-get-youtube-video-id
VIDEO_ID_RE = '(?<=(?:v|i)=)[a-zA-Z0-9-]+(?=&)|(?<=(?:v|i)\/)[^&\n]+|(?<=embed\/)[^"&\n]+|(?<=(?:v|i)=)[^&\n]+|(?<=youtu.be\/)[^&\n]+'

# Max feed collection size can be used to reduce the space of videos resulting from a search
# to increases cache hit probability.
MAX_FEED_COLLECTION_SIZE = 3

def extract_video_id_from_web_url(url):
    """
    Extracts video identifier from web url.

    >>> extract_video_id_from_web_url("http://www.youtube.com/watch?v=9bZkp7q19f0&feature=g-all-f&context=G27f364eFAAAAAAAAAAA")
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url("http://www.youtube.com/watch?feature=g-all-f&v=9bZkp7q19f0&context=G27f364eFAAAAAAAAAAA")
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url('<iframe width="560" height="315" src="http://www.youtube.com/embed/9bZkp7q19f0" frameborder="0" allowfullscreen></iframe>')
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url("youtube.com/v/9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url("youtube.com/vi/9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url("youtube.com/?v=9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url("youtube.com/?vi=9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url("youtube.com/watch?v=9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url("youtube.com/watch?vi=9bZkp7q19f0")
    '9bZkp7q19f0'
    >>> extract_video_id_from_web_url("youtu.be/9bZkp7q19f0")
    '9bZkp7q19f0'

    >>> extract_video_id_from_web_url("http://vimeo.com/48100473")
    Traceback (most recent call last):
        ...
    VideoIdentifierError: http://vimeo.com/48100473
    """

    matches = re.search(VIDEO_ID_RE,url)
    if matches is None:
        raise VideoIdentifierError(url)
    return matches.group(0)

def extract_video_id_from_api_uri(uri):
    """
    See https://developers.google.com/youtube/1.0/developers_guide_python#UnderstandingVideos

    >>> extract_video_id_from_api_uri("http://gdata.youtube.com/feeds/api/videos/9bZkp7q19f0")
    '9bZkp7q19f0'
    """
    return uri[-11:]

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
        self._best_streaming_url = None
        self._worst_streaming_url = None
        self._comments = None

    @classmethod
    def from_web_url(cls,url):
        """
        Constructs a Video object from a web url.

        :type url: string
        :rtype: Video
        """
        video_id = extract_video_id_from_web_url(url)
        entry = yt_service.GetYouTubeVideoEntry(video_id=video_id)
        return cls(entry)

    def __repr__(self):
        return "Video(title=%s, duration=%s)" % (self.title(), self.duration())

    def title(self):
        return self._entry.media.title.text

    def description(self):
        return self._entry.media.description.text

    def duration(self):
        return int(self._entry.media.duration.seconds)

    def related(self):
        """
        :rtype: VideoCollection
        """
        # See https://developers.google.com/youtube/1.0/developers_guide_python
        # See http://gdata-python-client.googlecode.com/hg/pydocs/gdata.youtube.service.html#YouTubeService-GetYouTubeRelatedVideoFeed
        # See http://gdata-python-client.googlecode.com/hg/pydocs/gdata.youtube.html#YouTubeVideoEntry
        
        # This should work however API doesn't recognise the URI.
        # related_feed = yt_service.GetYouTubeRelatedVideoFeed(uri=self._entry.id.text)
        
        # Instead get video_id from the URI.
        related_feed = yt_service.GetYouTubeRelatedVideoFeed(video_id=self.video_id())
        return VideoCollection.from_feed(related_feed)

    def video_id(self):
        """
        :rtype: string
        """
        return extract_video_id_from_api_uri(self._entry.id.text)

    def web_url(self):
        return self._entry.media.player.url

    def streaming_url(self, format):
        """
        Returns url for streaming video using specified format.
        """
        output = subprocess.check_output(["youtube-dl","--get-url","--format", format, self.web_url()])
        return output[:-1] # Remove new line character.

    def best_streaming_url(self):
        """
        Returns url for streaming video using best available format.

        Use memoisation for performance.
        """
        if self._best_streaming_url is None:
            self._best_streaming_url = self.streaming_url("best")
        return self._best_streaming_url

    def worst_streaming_url(self):
        """
        Returns url for streaming video using worst available format.

        Use memoisation for performance.
        """
        if self._worst_streaming_url is None:
            self._worst_streaming_url = self.streaming_url("worst")
        return self._worst_streaming_url

    def random_comment(self):
        """
        Uses memoisation for performance.

        :rtype: string
        """
        if self._comments is None:
            comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=self.video_id())
            self._comments = []
            for comment in comment_feed.entry:
                # Store comment body and author name
                self._comments.append("%s: %s" % (comment.author[0].name.text, comment.content.text))
        return random.choice(self._comments)

class VideoCollection(collections.Sequence):
    """
    An ordered collection of videos.

    This could be implemented by subclassing list however at this point not clear
    what the interface to VideoCollection should be. Will use delegation-composition
    and selectively build interface.

    self._videos : Video sequence
    """

    def __init__(self,videos=[]):
        """
        Does not enforce a maximum size.

        :type videos: Video iterable
        :rtype: VideoCollection
        """
        self._videos = []
        for video in videos:
            self._videos.append(video)

    @classmethod
    def from_feed(cls,feed):
        """
        Constructs a VideoCollection object from a YouTubeVideoFeed object.

        Enforces a maximum feed size.

        :type feed: gdata.youtube.YouTubeVideoFeed
        :rtype: VideoCollection
        """
        videos = []
        i = 0
        for entry in feed.entry:
            if i >= MAX_FEED_COLLECTION_SIZE:
                break
            videos.append(Video(entry))
            i += 1
        return cls(videos)

    @classmethod
    def from_web_urls(cls,urls):
        """
        Does not enforce a maximum size.

        :param urls: YouTube video web urls
        :type urls: String iterable
        :rtype: VideoCollection
        """
        return cls(map(Video.from_web_url, urls))

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

    def __repr__(self):
        # Only show first few as Video.__str__ is expensive
        videos = []
        i = 0
        for video in self:
            if i > 1:
                videos.append("...")
                break
            videos.append(video)
            i += 1
        return str(videos)

def search(search_terms):
    """
    :rtype: VideoCollection
    """
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.vq = search_terms
    # relevance, viewCount, published, or rating
    query.orderby = 'viewCount'
     # Exclude restricted content for child safety
    query.racy = 'exclude'
    feed = yt_service.YouTubeQuery(query)
    return VideoCollection.from_feed(feed)

def top_rated():
    """
    :rtype: VideoCollection
    """
    return VideoCollection.from_feed(yt_service.GetTopRatedVideoFeed())

def most_viewed():
    """
    :rtype: VideoCollection
    """
    return VideoCollection.from_feed(yt_service.GetMostViewedVideoFeed())

def recently_featured():
    """
    :rtype: VideoCollection
    """
    return VideoCollection.from_feed(yt_service.GetRecentlyFeaturedVideoFeed())

def most_recent():
    """
    :rtype: VideoCollection
    """
    return VideoCollection.from_feed(yt_service.GetMostRecentVideoFeed())