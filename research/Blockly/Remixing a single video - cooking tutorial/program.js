var currentVideo;
var video;
var duration;
var offset;
var speed;
var volume;
var allMusicVideos;
var i;

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


// The same video, a cooking video, is used throughout.
currentVideo = 'some cookery video with some irrelevant and some particularly interesting bits';
// Repeat the whole thing several times as user may want to review recipe
for (i = 0; i <= 9; i++) {
  // Start from 20s into the video
  play(currentVideo, 5, 20, 1, 10);
  for (i = 0; i <= 2; i++) {
    // Really important scene. PLay 3 times. Speech isn't important so can play it a bit faster and reduce the volume so the change of tone of speed isn't too distracting.
    play(currentVideo, 5, 25, 3, 2);
  }
  // Very similar to the first scene, not much interesting stuff left to do!
  play(currentVideo, 10, 30, 1, 10);
  // Play the first 10 s of the video at normal speed and volume.
  play(currentVideo, 10, 0, 1, 10);
  // Viewer may have had quite enough by this point! Allow them to quite the video.
  if (window.prompt('do you want to keep watching the video? (y/n)') != 'y') {
    break;
  }
}