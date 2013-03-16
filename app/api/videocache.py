"""
Video caching API.

init must be called before using other functions.
"""

import os
import logging
import subprocess
import time
import threading

from app import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Guarantees provided by cache.
MAX_NOT_CACHED_GET_TIME = 20 # seconds
MAX_CACHED_GET_TIME = 1 # seconds
MIN_VIDEO_READY_FILE_SIZE = long(0.1 * 2**20) # bytes, 0.1 MB

# Configuration partly externalised:
# config.CACHE_DIR
# config.FORMAT
_OUTPUT_TEMPLATE = "%(cache_dir)s/%(id)s.%(format)s"
_PRIMING_BATCH_SIZE = 1
_PRIMING_TIMEOUT = 60

_initialised = False

def init():
    logger.info("Initialising video cache.")
    global _initialised
    if not _initialised:
        logger.info("Not yet initialised, ensuring cache directories exist.")
        for location in [config.CACHE_DIR]:
            _ensure_dir_exists(location)
        _initialised = True

def clear():
    logger.info("Cleared cache.")
    for file_ in _get_all_cached_files():
        os.remove(file_)

def get(video):
    """
    Returns path to local copy of video.

    Uses cached file if possible. If it can't get the video from the cache it
    will will start a download and return path when enough of the video has
    been downloaded that playback could start from the beginning.

    :type video: youtube.Video
    """
    logger.info("get(%s)" % video)
    video_path = _find(video)
    if video_path is not None:
        return video_path
    else:
        video_path = _download(video, config.CACHE_DIR)
        # Busy wait until file is ready.
        # Assume won't be ready immediately.
        time.sleep(5)
        _wait_until_ready(video_path)
        return video_path

def prime(videos):
    """
    Prime the cache by pre loading a collection of videos.

    :type videos: youtube.Video iterable
    """
    logger.info("prime(%s)" % videos)

    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    # Download _PRIMING_BATCH_SIZE videos at a time.
    for videos_chunk in chunks(list(videos), _PRIMING_BATCH_SIZE):
        threads = []
        for video in videos_chunk:
            print video
            thread = threading.Thread(target=get, args=[video])
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join(_PRIMING_TIMEOUT)

    for video in videos:
        get(video)

def _is_ready(video_path):
    """
    Returns true if video at path is ready to be played.
    """
    return os.path.exists(video_path) and \
        os.path.isfile(video_path) and \
        os.access(video_path, os.R_OK) and \
        os.path.getsize(video_path) > MIN_VIDEO_READY_FILE_SIZE

def _wait_until_ready(video_path):
    """
    Busy wait until video is ready.
    """
    while not _is_ready(video_path):
        logger.info("%s not ready, waiting." % video_path)
        time.sleep(1)

def _ensure_dir_exists(dir_):
    """
    :type _dir: string
    """
    if not os.path.exists(dir_):
        os.makedirs(dir_)

def _get_all_cached_files():
    """
    :return: iterable of full path to cached files
    """
    files = []
    for location in [config.CACHE_DIR]:
        files.extend(map(lambda f: os.path.join(location, f), os.listdir(location)))
    return files

def _find(video):
    """
    :return: Path to local copy of video if in cache. Otherwise, None.
    """
    format = config.FORMAT

    # Peform a niave search, don't cache file paths.
    # Assume that file system lookup will be fast.
    for cache_dir in [config.CACHE_DIR]:
        video_path = _OUTPUT_TEMPLATE % {"cache_dir": cache_dir, "id": video.video_id(), "format": format}
        if os.path.exists(video_path):
            # To avoid race condition where download has only just started wait
            # until video is ready. No guarantee video is being downloaded so
            # may get stuck in infinite loop.
            _wait_until_ready(video_path)
            return video_path
    return None

def _download(video, cache_dir):
    """
    Downloads video into cache_dir and returns file path.

    Download runs asychronology so:
    - download will continue after function returns
    - no guarantees are given about the size of the file downloaded

    :type video: string
    :type cache_dir: string
    """
    logger.info("_download(%s, %s)" % (video, cache_dir))

    format = config.FORMAT

    # Need to leave id unchanged.
    output_template = _OUTPUT_TEMPLATE % {"cache_dir": cache_dir, "id": "%(id)s", "format": format}

    web_url = video.web_url()
    video_id = video.video_id()

    # Don't use part file so that it's easy to work out the output file path.
    p = subprocess.Popen(["youtube-dl", "--format", format, "--output", output_template, "--no-part", web_url])

    return output_template % {"id": video_id}
