"""
Videoplayer API.
"""

import time

def play(video,offset,duration):
    print "play(%s,%s,%s)" % (video,offset,duration)
    time.sleep(duration)