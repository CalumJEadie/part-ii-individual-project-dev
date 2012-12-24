"""
YouTube API.
"""

class Video:

    def title(self):
        pass

    def description(self):
        pass

    def duration(self):
        return -1

    def related(self):
        return VideoCollection()

class VideoCollection:

    def __init__(self,videos=[]):
        pass

    def random(self):
        """
        Return a random video from this collection.
        """
        return Video()