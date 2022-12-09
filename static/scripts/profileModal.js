var profileModal = document.getElementById("profileModal");

var modalBtn = document.getElementById("profileBtn");

var closeBtn = document.getElementsByClassName("close")[0];

modalBtn.onclick = function() {
    profileModal.style.display = "block";
}

closeBtn.onclick = function() {
    profileModal.style.display = "none";
}