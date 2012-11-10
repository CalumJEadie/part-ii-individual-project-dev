"""
Utilies.
"""

import subprocess
import os
import time

JOQAMP_DIR = "/opt/diss/jogamp/jogamp-all-platforms"

YOUTUBE_FORMATS = {
    "5" : "flv [240x400]",
    "17" : "mp4 [144x176]",
    "18" : "mp4 [360x640]",
    "22" : "mp4 [720x1280]",
    "34" : "flv [360x640]",
    "35" : "flv [480x854]",
    "37" : "mp4 [1080x1920]",
    "43" : "webm [360x640]",
    "44" : "webm [480x854]",
    "45" : "webm [720x1280]",
    "46" : "webm [1080x1920]",
    }

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
    return output[:-1] # Remove new line character.

def run_movie_cube(stream_url):
	"""
	Runs the JogAmp/JOGL movie cube demo.
	"""
	
	timeout = 20
	run_with_timeout(["java","-cp",
		"jar/jogl-all.jar:jar/gluegen-rt.jar:/usr/share/java/junit4.jar:jar/jogl-test.jar",
		"com/jogamp/opengl/test/junit/jogl/demos/es2/av/MovieCube",
		"-time","400000","-width","1980","-height","1080","-url",stream_url],timeout,cwd=JOQAMP_DIR)

def start(args,cwd=None):
	"""
	Runs command and returns pid.
	"""
	return subprocess.Popen(args,cwd=cwd).pid

def stop(pid):
	os.kill(pid,signal.SIGKILL)
	
def run_with_timeout(cmd,timeout,cwd=None):
    """
    Executes "cmd" and terminates after timeout has passed.
    """
    proc = subprocess.Popen(cmd,cwd=cwd)
    time.sleep(timeout)
    proc_status = proc.poll()
    if proc_status is None:
        proc.terminate()

def time_function(f):
    """
    Returns the time taken for f to execute.
    """
    start = time.time()
    f()
    end = time.time()
    return end-start

def run_timed_movie_cube(stream_url):
    """
    Runs the JoqAmp/JOGL movie cube demo and returns how long it took to execute.
    """

    def f():
        proc = subprocess.Popen(["java","-cp",
            "jar/jogl-all.jar:jar/gluegen-rt.jar:/usr/share/java/junit4.jar:jar/jogl-test.jar",
            "com/jogamp/opengl/test/junit/jogl/demos/es2/av/MovieCube",
            "-time","400000","-width","1980","-height","1080","-url",stream_url],
            cwd=JOQAMP_DIR)
        proc.wait()
    return time_function(f)

def run_timed_movie_cube_with_timeout(stream_url,timeout):
    """
    Runs the JoqAmp/JOGL movie cube demo and returns how long it took to execute.

    Execute terminated if run time exceeds timeout.
    """

    def f():
        run_with_timeout(["java","-cp",
            "jar/jogl-all.jar:jar/gluegen-rt.jar:/usr/share/java/junit4.jar:jar/jogl-test.jar",
            "com/jogamp/opengl/test/junit/jogl/demos/es2/av/MovieCube",
            "-time","400000","-width","1980","-height","1080","-url",stream_url],timeout,
            cwd=JOQAMP_DIR)
    return time_function(f)

def run_timed_omxplayer(stream_url):
    """
    Plays a video using Omxplayer and returns how long it took to execute.
    """

    def f():
        #print "omxplayer --refresh \'%s\'" % stream_url
        subprocess.call(["omxplayer","--refresh",stream_url],stderr=subprocess.STDOUT)
    return time_function(f)
