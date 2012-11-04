#!/usr/bin/python

import subprocess
import sys

# Configuration

WEB_URL = "http://www.youtube.com/watch?v=YE7VzlLtp-4" # Big Buck Bunny
# Format codes for YouTube / youtube-dl
FORMAT_CODES = {
	"webm_480p" : 43,
	"h264_mp4_480p": 18,
	"h264_flv_480p": 35,
	"3gp": 17
}

def main():
	pass

"""
Uses youtube-dl to get the streaming url.
"""
def get_streaming_url(web_url,format_code):	
	yt_dl = subprocess.Popen(['youtube-dl', '-g', url], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	(url, err) = yt_dl.communicate()
	if yt_dl.returncode != 0:
		sys.stderr.write(err)
		raise RuntimeError('Error getting URL.')


"""
Plays video within Movie Cube demo from JogAmp project.
"""
def run_movie_cube(format_code)
if __name__ == __main__:
	main()
