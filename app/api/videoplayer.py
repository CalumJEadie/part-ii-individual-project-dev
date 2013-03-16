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

#MIN_DURATION = 5 # worst
MIN_DURATION = 10 # 18
#MIN_DURATION = 15 # best
# Empirical time needed between starting OMXPlayer and it being able to process input
# Need rediculous wait for best quality video, presumably loading into memory
#OMXPLAYER_START_UP = 1.5 # worst
OMXPLAYER_START_UP = 5 # 18
#OMXPLAYER_START_UP = 9 # best
assert OMXPLAYER_START_UP < MIN_DURATION

# Use simple Python enum idiom to represent allows speeds.
class Speed():
    Slow = pyomxplayer.OMXPlayer.SLOW_SPEED
    Normal = pyomxplayer.OMXPlayer.NORMAL_SPEED
    Fast = pyomxplayer.OMXPlayer.FAST_SPEED
    VFast = pyomxplayer.OMXPlayer.VFAST_SPEED

def play(video, offset, duration, volume, speed):
    """
    :type video: youtube.Video
    :type offset: int
    :type duration: int
    :type volume: int
    :type speed: Speed
    """

    logger.info("play(video=%s, offset=%s, duration=%s, volume=%s, speed=%s)",video,offset,duration,volume, speed)

    # Inialise videocache.
    videocache.init()

    # Enforce minimum duration to make sure have time for OMXPlayer to start up
    # and begin playing.
    if duration < MIN_DURATION:
        duration = MIN_DURATION
        logger.info("Enforcing minimum duration of %s seconds" % MIN_DURATION)

    if pyomxplayer.is_omxplayer_available():
        video_path = videocache.get(video)
        logger.info("OMXPlayer(%s)" % video_path)
        p = pyomxplayer.OMXPlayer(video_path)
        # Delaying changes to give OMXPlayer time to set up and be ready to accept input
        time.sleep(OMXPLAYER_START_UP)
        p.seek(offset)
        p.set_volume(volume)
        p.set_speed(speed)
        time.sleep(duration-OMXPLAYER_START_UP)
        p.stop()
    else:
        logger.info("OMXPlayer not available, calling `time.sleep`.")
        time.sleep(duration)
