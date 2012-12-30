# This program displays the title and description for Gangnam Style.
gangnam_style_url = "http://www.youtube.com/watch?v=9bZkp7q19f0"
video = youtube.Video.from_web_url(gangnam_style_url)
display(video.title(),1)
display(video.duration(),1)