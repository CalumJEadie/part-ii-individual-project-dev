#!/usr/bin/python

"""
Unit tests for the util module.
"""

import unittest

import util
import videos

class Test(unittest.TestCase):

	@unittest.skip('')
	def test_get_available_formats(self):
		formats = util.get_available_formats(videos.BBB_ORIGINAL)
		print formats

	@unittest.skip('')
	def test_get_streaming_url(self):
		formats = util.get_available_formats(videos.BBB_ORIGINAL)
		streaming_url = util.get_streaming_url(videos.BBB_ORIGINAL,formats[0])
		print streaming_url
	
	def test_run_movie_cube(self):
		formats = util.get_available_formats(videos.BBB_ORIGINAL)
        streaming_url = util.get_streaming_url(videos.BBB_ORIGINAL,formats[0])
		util.run_movie_cube(streaming_url)

if __name__ == "__main__":
		unittest.main(verbosity=2)
