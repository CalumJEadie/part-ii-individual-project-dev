"""
Video caching API.

init must be called before using other functions.
"""

import os
import logging
import subprocess
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_CACHE_DIR = "/tmp/diss/videocache"
_OUTPUT_TEMPLATE = "%(cache_dir)s/%(id)s"

def init():
    logger.info("Initialising video cache.")
    for location in [_CACHE_DIR]:
        _ensure_dir_exists(location)

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
        video_path = _download(video, _CACHE_DIR)
        # Wait until 1 MB of file has been downloaded.
        # Do this niavely by waiting for a time period.
        time.sleep(9)
        return video_path

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
    for location in [_CACHE_DIR]:
        files.extend(map(lambda f: os.path.join(location, f), os.listdir(location)))
    return files

def _find(video):
    """
    :return: Path to local copy of video if in cache. Otherwise, None.
    """
    # Peform a niave search, don't cache file paths.
    # Assume that file system lookup will be fast.
    for cache_dir in [_CACHE_DIR]:
        video_path = _OUTPUT_TEMPLATE % {"cache_dir": cache_dir, "id": video.video_id()}
        if os.path.exists(video_path):
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

    # Need to leave id unchanged.
    output_template = _OUTPUT_TEMPLATE % {"cache_dir": cache_dir, "id": "%(id)s"}

    format = "worst"

    web_url = video.web_url()
    video_id = video.video_id()

    # Don't use part file so that it's easy to work out the output file path.
    p = subprocess.Popen(["youtube-dl", "--format", format, "--output", output_template, "--no-part", web_url])

    return output_template % {"id": video_id}