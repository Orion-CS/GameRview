window.addEventListener("DOMContentLoaded", async () => {
    window.myNameSpace = {};

    window.myNameSpace.counter = 0;
    const starButton1 = document.getElementById("star1");
    const starButton2 = document.getElementById("star2");
    const starButton3 = document.getElementById("star3");
    const starButton4 = document.getElementById("star4");
    const starButton5 = document.getElementById("star5");
    starButton1.addEventListener("click", fill_in1);
    starButton2.addEventListener("click", fill_in2);
    starButton3.addEventListener("click", fill_in3);
    starButton4.addEventListener("click", fill_in4);
    starButton5.addEventListener("click", fill_in5);

});

function fill_in1() {
    starButton1.style.color = "yellow";
}

function fill_in2() {
    starButton2.style.color = "yellow";
}

function fill_in3() {
    starButton3.style.color = "yellow";
}

function fill_in4() {
    starButton4.style.color = "yellow";
}

function fill_in5() {
    starButton5.style.color = "yellow";
}
