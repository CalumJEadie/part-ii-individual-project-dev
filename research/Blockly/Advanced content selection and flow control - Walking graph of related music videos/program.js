var video;
var duration;
var offset;
var speed;
var volume;
var currentVideo;
var allMusicVideos;
var i;
var responce;

function math_random_int(a, b) {
  if (a > b) {
    // Swap a and b to ensure a is smaller.
    var c = a;
    a = b;
    b = c;
  }
  return Math.floor(Math.random() * (b - a + 1) + a);
}

function get_duration_of(video) {
  return math_random_int(30, 120);
}

function play(video, duration, offset, speed, volume) {
  window.alert([video,', ',duration,', ',offset,', ',speed,', ',volume].join(''));
}

function get_title_of(video) {
  return video;
}

function get_related(video) {
  return get_random_music_video();
}

function get_random_music_video() {
  allMusicVideos = ['psy - gangnam style', 'miley cyrus - can\'t be tamed', 'gotye - somebody that i used to know', 'etc...'];
  return allMusicVideos[math_random_int(1, allMusicVideos.length) - 1];
}


currentVideo = get_random_music_video();
for (i = 0; i <= 2; i++) {
  currentVideo = get_related(currentVideo);
  window.alert(get_title_of(currentVideo));
  play(currentVideo, math_random_int(5, get_duration_of(currentVideo) / 2), 0, 1, 10);
  responce = window.prompt('did you like those songs? (y/n)');
  // If user didn't like the previous videos then change to a different seed video.
  if (responce == 'y') {
    currentVideo = get_random_music_video();
  }
}
