import random

video = None
duration = None
offset = None
speed = None
volume = None
currentVideo = None
allMusicVideos = None
i = None
responce = None

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


currentVideo = get_random_music_video()
for i in range(3):
  currentVideo = get_related(currentVideo)
  print(get_title_of(currentVideo))
  play(currentVideo, random.randint(5, get_duration_of(currentVideo) / 2), 0, 1, 10)
  responce = text_prompt('did you like those songs? (y/n)')
  # If user didn't like the previous videos then change to a different seed video.
  if responce == 'y':
    currentVideo = get_random_music_video()
