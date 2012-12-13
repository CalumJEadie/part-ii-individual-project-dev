import random

currentVideo = None
video = None
duration = None
offset = None
speed = None
volume = None
allMusicVideos = None
i = None

def text_prompt(msg):
  try:
    return raw_input(msg)
  except NameError:
    return input(msg)

def get_duration_of(video):
  return random.randint(30, 120)

def play(video, duration, offset, speed, volume):
  print(''.join([str(temp_value) for temp_value in [video, ', ', duration, ', ', offset, ', ', speed, ', ', volume]]))

def get_title_of(video):
  return video

def get_related(video):
  return get_random_music_video()

def get_random_music_video():
  global allMusicVideos
  allMusicVideos = ['psy - gangnam style', 'miley cyrus - can\'t be tamed', 'gotye - somebody that i used to know', 'etc...']
  return allMusicVideos[random.randint(1, len(allMusicVideos)) - 1]


# The same video, a cooking video, is used throughout.
currentVideo = 'some cookery video with some irrelevant and some particularly interesting bits'
# Repeat the whole thing several times as user may want to review recipe
for i in range(10):
  # Start from 20s into the video
  play(currentVideo, 5, 20, 1, 10)
  for i in range(3):
    # Really important scene. PLay 3 times. Speech isn't important so can play it a bit faster and reduce the volume so the change of tone of speed isn't too distracting.
    play(currentVideo, 5, 25, 3, 2)
  # Very similar to the first scene, not much interesting stuff left to do!
  play(currentVideo, 10, 30, 1, 10)
  # Play the first 10 s of the video at normal speed and volume.
  play(currentVideo, 10, 0, 1, 10)
  # Viewer may have had quite enough by this point! Allow them to quite the video.
  if text_prompt('do you want to keep watching the video? (y/n)') != 'y':
    break