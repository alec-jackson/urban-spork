/*
Jatas.org Style pack
Written By:
Alec Jackson
Ryan Taylor
 */

function navExpand() {
  var newWindowWidth = (window.innerWidth > 0) ? window.innerWidth : screen.width;
  if( newWindowWidth > 600) {
    return;
  }

  var x = document.getElementById("nav");
  if (x.style.height === "300px") {
    x.style.height = "60px";
  } else {
    document.getElementById('nav').style.WebkitTransition = '1s';
    document.getElementById('nav').style.MozTransition = '1s';
    x.style.height = "300px";
  }
}
