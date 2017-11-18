"use strict";

function updateTime(start) {
    let elapsed = Date.now() - start;
    let seconds = Math.floor(elapsed / 1000);
    let minutes = Math.floor(seconds / 60);
    let hours = Math.floor(minutes / 60);
  
    minutes = "0" + String(minutes % 60);
    seconds = "0" + String(seconds % 60);

    let display = `${hours}:${minutes.slice(-2)}:${seconds.slice(-2)}`;
    $("#time").html(display);
}

function initTimer() {
    let start = Date.parse("13 Nov 2017 16:00:00 UTC");
    updateTime(start);
    let interval = setInterval(function () {
        updateTime(start);
    }, 1000);
}

window.addEventListener("DOMContentLoaded", function () {
    initTimer();
});