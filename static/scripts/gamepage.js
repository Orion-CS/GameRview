window.addEventListener("DOMContentLoaded", async () => {
    window.myNameSpace = {};

    window.myNameSpace.counter = 0;

    let starsContainer = document.getElementById("stars");
    let reviews = document.getElementsByClassName("reviews");
    

    for(let j=0; j<reviews.length; j++){ 
        for (let i=0; i<5 ;i++){
            let value = reviews[j].querySelector('#review-rating').innerHTML[0];
            let starImg = document.createElement("img");
            if(i<=value-1){
                starImg.src = "/static/icons/star.png"
            }else{
               starImg.src = "/static/icons/stargray.png"; 
            }
            starImg.className = "star-style";
            reviews[j].querySelector('#stars').appendChild(starImg);
        }       
    };
});

