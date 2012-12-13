import random

video = None
duration = None
offset = None
speed = None
volume = None
videos = None
keywords = None
i = None
list2 = None
all_wedding_videos = None
currentVideo = None

def get_duration_of(video):
    return random.randint(30, 120)

def get_title_of(video):
    return video

def play(video, duration, offset, speed, volume):
    print(''.join([str(temp_value) for temp_value in [video, ', ', duration, ', ', offset, ', ', speed, ', ', volume]]))

def get_related(video):
    return get_random_wedding_video()

def get_random_wedding_video():
    global all_wedding_videos
    all_wedding_videos = ['a christian wedding video', 'an islamic wedding video', 'a jewish wedding video', 'etc...']
    return get_random_item(all_wedding_videos)

def top_100_of(videos):
    return videos

def select_randomly_from(videos):
    return get_random_item(videos)

def search(keywords):
    global all_wedding_videos
    all_wedding_videos = ['a christian wedding video', 'an islamic wedding video', 'a jewish wedding video', 'etc...']
    return all_wedding_videos

def get_random_item(list2):
    return list2[random.randint(1, len(list2)) - 1]


for i in range(3):
    currentVideo = select_randomly_from(top_100_of(search('wedding christianity')))
    print(get_title_of(currentVideo))
    play(currentVideo, get_duration_of(currentVideo) / 2, random.randint(0, get_duration_of(currentVideo) / 2), 1, 10)
    currentVideo = select_randomly_from(top_100_of(search('wedding islam')))
    print(get_title_of(currentVideo))
    play(currentVideo, get_duration_of(currentVideo) / 2, random.randint(0, get_duration_of(currentVideo) / 2), 1, 10)
    currentVideo = select_randomly_from(top_100_of(search('wedding judaism')))
    print(get_title_of(currentVideo))
    play(currentVideo, get_duration_of(currentVideo) / 2, random.randint(0, get_duration_of(currentVideo) / 2), 1, 10)