window.addEventListener("DOMContentLoaded", async () => {
    window.myNameSpace = {};

    window.myNameSpace.counter = 0;
    const starButton1 = document.getElementById("star1");
    starButton1.addEventListener("click", fill_in1);
});