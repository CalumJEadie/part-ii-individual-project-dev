#!/usr/bin/python

"""
Tests the performance of the GPU for lower resolution video formats and the ability to interact
with other programs while JogAmp controls part of the screen.

Streams YouTube video in different formats and plays using the JOGL Movie Cube demo,
which is being used a black box to measure video performance.
"""

import argparse
import sys
import logging

import util

#TIMEOUT = 60
FORMATS = [
    '18', # MP4 H.264/AAC 360x640
    '43', # WEBM VP8/Vorbis 360x640
    '5' # FLV H.263/MP3 240x400
]
WIDTH = 640
HEIGHT = 360

def main():

    logger = get_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument("web_url",help="url of YouTube video used on website")
    args = parser.parse_args(sys.argv[1:])
    web_url = args.web_url

    available_formats = util.get_available_formats(web_url)
    print available_formats
    logger.info("available_formats : %s" % available_formats)

    testable_formats = set(available_formats) & set(FORMATS)
    logger.info("testable_formats : %s" % testable_formats)

    logger.info("width: %s, height: %s" % (WIDTH,HEIGHT))

    for fmt in testable_formats:
        logger.info("Format: %s, %s" % (fmt,util.YOUTUBE_FORMATS[fmt]))
        streaming_url = util.get_streaming_url(web_url,fmt)
        logger.info("Streaming URL: %s" % streaming_url)
        run_time = util.run_timed_movie_cube(streaming_url,WIDTH,HEIGHT)
        logger.info("Run time for [%s,%s]: %s" % (fmt,util.YOUTUBE_FORMATS[fmt],run_time))

def get_logger():
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(__file__+'.log')
    formatter = logging.Formatter('\n\n%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

if __name__ == "__main__":
    main()
