var red_car_video;
var video;
var duration;
var offset;
var speed;
var volume;
var allMusicVideos;
var green_car_video;
var current_duration;
var current_offset;
var i;

function play(video, duration, offset, speed, volume) {
  window.alert([video,', ',duration,', ',offset,', ',speed,', ',volume].join(''));
}

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


red_car_video = 'red car video';
green_car_video = 'green car video';
current_duration = get_duration_of(red_car_video) / 4;
current_offset = 0;
for (i = 0; i <= 9; i++) {
  play(red_car_video, current_duration, current_offset, 1, 10);
  current_offset = current_offset + current_duration;
  play(red_car_video, current_duration, current_offset, 1, 10);
  current_offset = current_offset + current_duration;
  current_duration = current_duration / 2;
}