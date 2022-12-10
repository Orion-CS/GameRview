var profileModal = document.getElementById("profileModal");

var modalBtn = document.getElementById("profileBtn");

var closeBtn = document.getElementsByClassName("close")[0];

if (modalBtn != null) {
    modalBtn.onclick = function() {
        profileModal.style.display = "block";
    }
}

if (closeBtn != null) {
    closeBtn.onclick = function() {
        profileModal.style.display = "none";
    }
}