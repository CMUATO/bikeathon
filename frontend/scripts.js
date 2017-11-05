function updateTime(start) {
    let elapsed = Date.now() - start;
    let seconds = Math.floor(elapsed / 1000);
    let minutes = Math.floor(seconds / 60);
    let hours = Math.floor(minutes / 60);
    let days = Math.floor(hours / 24);

    let display = `${days}:${hours % 24}:${minutes % 60}:${seconds % 60}`;
    $("#time-display").html(display);
}


function initTimer() {
    let start = Date.parse("4 Nov 2017 21:30:00 UTC");
    updateTime(start);
    let interval = setInterval(function () {
        updateTime(start);
    }, 1000);
}


window.addEventListener("DOMContentLoaded", function () {
    initTimer();
});