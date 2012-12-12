var video;
var duration;
var offset;
var speed;
var volume;
var videos;
var keywords;
var i;
var list;
var all_wedding_videos;
var currentVideo;

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

function play(video, duration, offset, speed, volume) {
  window.alert([video,', ',duration,', ',offset,', ',speed,', ',volume].join(''));
}

function get_related(video) {
  return get_random_wedding_video();
}

function get_random_wedding_video() {
  all_wedding_videos = ['a christian wedding video', 'an islamic wedding video', 'a jewish wedding video', 'etc...'];
  return get_random_item(all_wedding_videos);
}

function top_100_of(videos) {
  return videos;
}

function select_randomly_from(videos) {
  return get_random_item(videos);
}

function search(keywords) {
  all_wedding_videos = ['a christian wedding video', 'an islamic wedding video', 'a jewish wedding video', 'etc...'];
  return all_wedding_videos;
}

function get_random_item(list) {
  return list[math_random_int(1, list.length) - 1];
}


for (i = 0; i <= 2; i++) {
  currentVideo = select_randomly_from(top_100_of(search('wedding christianity')));
  window.alert(get_title_of(currentVideo));
  play(currentVideo, get_duration_of(currentVideo) / 2, math_random_int(0, get_duration_of(currentVideo) / 2), 1, 10);
  currentVideo = select_randomly_from(top_100_of(search('wedding islam')));
  window.alert(get_title_of(currentVideo));
  play(currentVideo, get_duration_of(currentVideo) / 2, math_random_int(0, get_duration_of(currentVideo) / 2), 1, 10);
  currentVideo = select_randomly_from(top_100_of(search('wedding judaism')));
  window.alert(get_title_of(currentVideo));
  play(currentVideo, get_duration_of(currentVideo) / 2, math_random_int(0, get_duration_of(currentVideo) / 2), 1, 10);
}
