<!--invisible close icon-->
document.getElementById("close_icon").style.display = "none";

function openNav() {
    if (window.screen.width < 800) {
        document.getElementById("mySidenav").style.width = "50%";
    } else {
        document.getElementById("mySidenav").style.width = "450px";
    }
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

//get the image url
let imageUrl = document.getElementById('background').title;
// document.getElementById('backgrounds').style.backgroundImage = "linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1))," + "url(" + imageUrl + ")";
document.getElementById('background').style.backgroundImage = "url(" + imageUrl + ")";

