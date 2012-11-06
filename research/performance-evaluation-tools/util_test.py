#!/usr/bin/python

"""
Unit tests for the util module.
"""

import unittest

import util

BBB_ORIGINAL = "http://www.youtube.com/watch?v=YE7VzlLtp-4" # Blender Foundation / Big Buck Bunny 

class Test(unittest.TestCase):

	@unittest.skip('')
	def test_get_available_formats(self):
		formats = util.get_available_formats(BBB_ORIGINAL)
		print formats

	@unittest.skip('')
	def test_get_streaming_url(self):
		formats = util.get_available_formats(BBB_ORIGINAL)
		streaming_url = util.get_streaming_url(BBB_ORIGINAL,formats[0])
		print streaming_url
	
	def test_run_movie_cube(self):
		formats = util.get_available_formats(BBB_ORIGINAL)
		streaming_url = util.get_streaming_url(BBB_ORIGINAL,formats[0])
		util.run_movie_cube(streaming_url)

if __name__ == "__main__":
		unittest.main(verbosity=2)
