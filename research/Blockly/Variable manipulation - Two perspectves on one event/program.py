import random

red_car_video = None
video = None
duration = None
offset = None
speed = None
volume = None
allMusicVideos = None
green_car_video = None
current_duration = None
current_offset = None
i = None

def play(video, duration, offset, speed, volume):
  print(''.join([str(temp_value) for temp_value in [video, ', ', duration, ', ', offset, ', ', speed, ', ', volume]]))

def get_duration_of(video):
  return random.randint(30, 120)

def get_title_of(video):
  return video

def get_related(video):
  return get_random_music_video()

def get_random_music_video():
  global allMusicVideos
  allMusicVideos = ['psy - gangnam style', 'miley cyrus - can\'t be tamed', 'gotye - somebody that i used to know', 'etc...']
  return allMusicVideos[random.randint(1, len(allMusicVideos)) - 1]


red_car_video = 'red car video'
green_car_video = 'green car video'
current_duration = get_duration_of(red_car_video) / 4
current_offset = 0
for i in range(10):
  play(red_car_video, current_duration, current_offset, 1, 10)
  current_offset = current_offset + current_duration
  play(red_car_video, current_duration, current_offset, 1, 10)
  current_offset = current_offset + current_duration
  current_duration = current_duration / 2