#!/usr/bin/python

"""
Tests the performance of the GPU for different video formats.

Streams YouTube video in different formats and plays using the JOGL Movie Cube demo,
which is being used a black box to measure video performance.
"""

import argparse
import sys
import logging

import util

#TIMEOUT = 60

def main():

    logger = get_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument("web_url",help="url of YouTube video used on website")
    args = parser.parse_args(sys.argv[1:])
    web_url = args.web_url

    formats = util.get_available_formats(web_url)

    for fmt in formats:
        logger.info("Format: %s, %s" % (fmt,util.YOUTUBE_FORMATS[fmt]))
        streaming_url = util.get_streaming_url(web_url,fmt)
        logger.info("Streaming URL: %s" % streaming_url)
        run_time = util.run_timed_movie_cube(streaming_url)
        logger.info("Run time for [%s,%s]: %s" % (fmt,util.YOUTUBE_FORMATS[fmt],run_time))

def get_logger():
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(__name__+'.log')
    formatter = logging.Formatter('\n\n%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

if __name__ == "__main__":
    main()
