window.addEventListener("DOMContentLoaded", async () => {
    var profileModal = document.getElementById("profileModal");

    var modalBtn = document.getElementById("profileBtn");

    var closeSpan = document.getElementsByClassName("close")[0];

    modalBtn.onclick = function() {
        profileModal.style.display= "block";
    }

    closeSpan.onclick = function() {
        profileModal.style.display = "none";
    }
});