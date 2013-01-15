"""
Videoplayer API.
"""

import logging
import time
import distutils.spawn

import pyomxplayer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def play(video,offset,duration):
    logger.info("play(video=%s,offset=%s,duration=%s)",video,offset,duration)
    if pyomxplayer.is_omxplayer_available():
        p = pyomxplayer.OMXPlayer(video)
        time.sleep(duration)
        p.stop()
    else:
        logger.info("OMXPlayer not available, calling `time.sleep`.")
        time.sleep(duration)