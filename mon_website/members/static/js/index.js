function simulateHoverOnContact(id) {
  var contactLink = document.getElementById(id);
  if (contactLink) {
    contactLink.style.color = 'red';
    setTimeout(function () {
      contactLink.style.color = 'black';
    }, 2000);
  }
}

var ids = ["Calendar", "Carousel", "Carouge", "Carreaux", "Caroline", "Carrefour"];
var currentIndex = 0;


function cycleIds() {
  simulateHoverOnContact(ids[currentIndex]);
  currentIndex = (currentIndex + 1) % ids.length;
}

/* Toggle Button to Unmute the Video */
function toggleMute() {
  var video = document.getElementById('video');
  if (video.muted) {
    video.muted = false;
  } else {
    video.muted = true;
  }
}

/* Delay Function to Add SetTimeOut After Defined Interval */
function delay(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

/* Show Video Function to Add Display Property to Show the Video on Click of Button which will fulfill User Interaction Needs to Browser to Run the Video with Unmute State */
function showVideo() {
  var element = document.getElementById('video'); 
  var videoUrl = element.getAttribute("data-video-url");
  element.src = videoUrl; 
  var button = document.getElementById('button');
  element.style.display = 'block';
  button.style.display = 'none';
  delay(100)
    .then(() => toggleMute())
    .then(() => {
      element.addEventListener('ended', function () {
        // When the video ends, rewind it to the beginning and play again
        element.currentTime = 0;
        element.play();
      });
    });
  cycleIds();
  setInterval(cycleIds, 3000);
}
