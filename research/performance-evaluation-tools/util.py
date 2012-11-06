"""
Utilies.
"""

import subprocess
import os
import time

JOQAMP_DIR = "/opt/diss/jogamp/jogamp-all-platforms"

def get_available_formats(web_url):
	"""
	Returns a list of available formats for the specified YouTube web url.
	"""
	output = subprocess.check_output(["youtube-dl","--get-format","--all-formats",web_url])
	return output.split('\n')[:-1]

def get_streaming_url(web_url,fmt):
	"""
	Returns the url to stream a YouTube video using specified format.
	"""
	output = subprocess.check_output(["youtube-dl","--get-url","--format",fmt,web_url])
	return output

def run_movie_cube(stream_url):
	"""
	Runs the JogAmp/JOGL movie cube demo.
	"""
	timeout = 20

	proc = subprocess.Popen(["java","-cp",
		"jar/jogl-all.jar:jar/gluegen-rt.jar:/usr/share/java/junit4.jar:jar/jogl-test.jar",
		"com/jogamp/opengl/test/junit/jogl/demos/es2/av/MovieCube",
		"-time","400000","-width","1980","-height","1080","-url",stream_url],
		cwd=JOQAMP_DIR)
	time.sleep(timeout)
	proc_status = proc.poll()
	if proc_status is None:
		proc.terminate()

def start(args,cwd=None):
	"""
	Runs command and returns pid.
	"""
	return subprocess.Popen(args,cwd=cwd).pid

def stop(pid):
	os.kill(pid,signal.SIGKILL)
