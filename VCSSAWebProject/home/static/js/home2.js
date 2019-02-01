<!--invisible close icon-->
document.getElementById("close_icon").style.display = "true";

//get the image url
var imageUrl = document.getElementById('background').title;
// document.getElementById('background').style.backgroundImage = "linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1))," + "url(" + imageUrl + ")";
document.getElementById('background').style.backgroundImage = "url(" + imageUrl + ")";


