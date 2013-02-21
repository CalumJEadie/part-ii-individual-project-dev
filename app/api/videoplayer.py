"""
Videoplayer API.
"""

import logging
import time
import distutils.spawn

import pyomxplayer

from app.api import videocache

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MIN_DURATION = 5

def play(video, offset, duration, volume):
    """
    :type video: youtube.Video
    :type offset: int
    :type duration: int
    :type volume: int
    """

    logger.info("play(video=%s, offset=%s, duration=%s, volume=%s)",video,offset,duration)

    # Inialise videocache.
    videocache.init()

    # Enforce minimum duration to make sure have time for OMXPlayer to start up
    # and begin playing.
    if duration < MIN_DURATION:
        duration = MIN_DURATION
        logger.info("Enforcing minimum duration of %ss" % MIN_DURATION)

    if pyomxplayer.is_omxplayer_available():
        video_path = videocache.get(video)
        logger.info("OMXPlayer(%s)" % video_path)
        p = pyomxplayer.OMXPlayer(video_path)
        p.set_volume(volume)
        time.sleep(duration)
        p.stop()
    else:
        logger.info("OMXPlayer not available, calling `time.sleep`.")
        time.sleep(duration)