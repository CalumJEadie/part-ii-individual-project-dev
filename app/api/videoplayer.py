"""
Videoplayer API.
"""

import logging
import time
import distutils.spawn

import pyomxplayer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MIN_DURATION = 10

def play(video,offset,duration):
    """
    :type video: youtube.Video
    """

    logger.info("play(video=%s,offset=%s,duration=%s)",video,offset,duration)

    # Enforce minimum duration to make sure have enough time to run `video.best_streaming_url()`.
    if duration < MIN_DURATION:
        duration = MIN_DURATION
        log.info("Enforcing minimum duration of %ss" % MIN_DURATION)

    if pyomxplayer.is_omxplayer_available():
        p = pyomxplayer.OMXPlayer(video.best_streaming_url())
        time.sleep(duration)
        p.stop()
    else:
        logger.info("OMXPlayer not available, calling `time.sleep`.")
        time.sleep(duration)