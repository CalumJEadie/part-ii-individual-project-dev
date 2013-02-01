"""
Unit tests for interpreter component.
"""

import unittest
import logging

from app.interpreter import interpreter

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Test(unittest.TestCase):

    def test_youtube(self):
        """
        Test interpreter using straight line code accessing the YouTube API.
        """

        code = '''gangnam_style_url = "http://www.youtube.com/watch?v=9bZkp7q19f0"
video = youtube.Video.from_web_url(gangnam_style_url)
print video.title()
print video.duration()'''
        interpreter.interpret(code)

    def test_function_call_outside_function(self):
        code = '''def f():
    print "f()"

f()'''
        interpreter.interpret(code)

    def test_function_call_inside_function(self):
        code = '''def f():
    print "f()"

def g():
    print "g()"
    f()

f()
g()'''
        interpreter.interpret(code)


if __name__ == "__main__":
    unittest.main()