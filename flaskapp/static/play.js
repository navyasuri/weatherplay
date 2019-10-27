base_url = window.location.origin || "localhost:5000";
isPlaying = true;

setInterval(() => {
  location.reload();
}, 15000)

function navigateTrack(direction) {
  $.get(
    base_url + '/navigate/' + direction,
    function () {
        if (direction != 'play') {
          location.reload()
        } else {
          if (isPlaying) {
            $('#playBtn').addClass('glyphicon-play').removeClass('glyphicon-pause');
          } else {
            $('#playBtn').addClass('glyphicon-pause').removeClass('glyphicon-play');
          }
          isPlaying = !isPlaying;
        }
    }
  );
}