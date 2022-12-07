window.addEventListener("DOMContentLoaded", async () => {
    window.myNameSpace = {};

    window.myNameSpace.counter = 0;
})

let responseField = document.getElementById('rating');
let starsContainer = document.getElementById("stars");
let active = -1

responseField.addEventListener("click", () => onDropClick(0))

for (let i=0; i<5 ;i++){
    let starImg = document.createElement("img");
    starImg.src = "/static/icons/stargray.png";
    starImg.className = "star-style";
    starsContainer.appendChild(starImg);

    starImg.addEventListener("mouseover", () => onStarHover(i));
    starImg.addEventListener("mouseleave", onStarOut);
    starImg.addEventListener("click", () => onStarClick(i));
}

let stars = document.querySelectorAll(".star-style");

function onDropClick(i){
let responseField = document.getElementById('rating');
i = responseField.value-1
console.log(i);
fixStars(i);
}

function onStarHover(i){
fill(i);
}

function fill(ratingVal){
    for(let i=0; i<5 ;i++){
        if(i<=ratingVal){
            stars[i].src = "/static/icons/star.png"
        }else{
            stars[i].src = "/static/icons/stargray.png"
        }
    }
}

function fixStars(ratingVal){
    let responseField = document.getElementById('rating');
    if(responseField.value != ratingVal){
            active = ratingVal;
            fill(active);
    }
}

function onStarOut(){
    fill(active);
}

function onStarClick(i){
    active = i
    let responseField = document.getElementById('rating');
    responseField.value = i+1;
    fill(active);
}
