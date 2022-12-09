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

    const favoriteButton = document.getElementById("favorite-button");
    favoriteButton.addEventListener("click", toggleFavorite);

    setupFavorite();
});

function toggleFavorite() {
    const gameIdText = document.getElementById("game-id");
    const gameId = gameIdText.innerText

    const userIdText = document.getElementById("user-id");
    const userId = userIdText.innerText

    var send_data = [
        {"gameId": gameId},
        {"userId": userId}
      ];

    console.log("HERE 1")

    $.ajax({
        type: "POST",
        url: "/toggleFavorite/",
        data: JSON.stringify(send_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            setFavorite(result)
          } 
    });
}

function setupFavorite() {
    const gameIdText = document.getElementById("game-id");
    const gameId = gameIdText.innerText

    const userIdText = document.getElementById("user-id");
    const userId = userIdText.innerText

    var send_data = [
        {"gameId": gameId},
        {"userId": userId}
      ];

    $.ajax({
        type: "POST",
        url: "/getFavorite/",
        data: JSON.stringify(send_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            setFavorite(result)
          } 
    });
}

function setFavorite(result) {
    const favoriteButton = document.getElementById("favorite-button");

    // check if is favorite
    if (result.favorite) {
        favoriteButton.innerText = "Un-Favorite"
    } else {
        favoriteButton.innerText = "Favorite"
    }
}