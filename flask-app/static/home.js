function wordHL() {
    if (document.getElementById("userinp").value.toLowerCase() === "good") {
        document.getElementById("userinp").style.color = "rgb(255, 226, 239)";
    } else if (document.getElementById("userinp").value.toLowerCase() === "bad"){
        document.getElementById("userinp").style.color = "rgb(91, 80, 127)";
    } else {
        document.getElementById("userinp").style.color = "rgb(0,0,0)";
    }
}

document.getElementById("userinp").addEventListener("input", wordHL);