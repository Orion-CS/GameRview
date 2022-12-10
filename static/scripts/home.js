window.addEventListener("DOMContentLoaded", async () => {
    window.myNameSpace = {};

    window.myNameSpace.counter = 0;

    let game = document.getElementsByClassName("d-sm-block");
    let other = document.getElementsByClassName("d-block")
    for (let i=0; i<game.length; i++){
        other[i].addEventListener("mouseover", () => jameRating(game[i]));
    }
});



function jameRating(game){
    let tester = game.querySelector('#tester');
    if (tester == null ) {
        let V = game.querySelector('#text').innerText[0];
        if(V>=0){
            for (let i=0; i<5 ;i++){
            let starImg = document.createElement("img");
            if(i<=V-1){
                starImg.src = "/static/icons/star.png"
            }else{
            starImg.src = "/static/icons/stargray.png"; 
            }
            starImg.className = "star-style";
            game.querySelector('#tstars').appendChild(starImg);
        }  
        
        }else{
            let noRating = document.createElement("div")
            noRating.innerText = "no reviews yet"
            game.querySelector('#tstars').appendChild(noRating);
        }
        let current = document.createElement("p");
        current.id="tester"
        current.hidden;
        game.querySelector('#tstars').appendChild(current);
        document.getElementById("text").hidden;
    }

    
}