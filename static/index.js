function intro_fade_in() {
    document.getElementById("intro").children[0].className += " load";
}

window.onload = intro_fade_in;
setTimeout(function() {
    window.location='/home'
}, 4000);