window.addEventListener("DOMContentLoaded", async () => {
    window.myNameSpace = {};

    const friendButton = document.getElementById("friend-button");
    friendButton.addEventListener("click", toggleFriend);

    setupFriend();
});

function toggleFriend() {
    const friendIdText = document.getElementById("friend-id");
    const friendId = friendIdText.innerText

    const userIdText = document.getElementById("user-id");
    const userId = userIdText.innerText

    var send_data = [
        {"friendId": friendId},
        {"userId": userId}
      ];

    $.ajax({
        type: "POST",
        url: "/toggleFriend/",
        data: JSON.stringify(send_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            setFriend(result)
          } 
    });
}

function setupFriend() {
    const friendIdText = document.getElementById("friend-id");
    const friendId = friendIdText.innerText

    const userIdText = document.getElementById("user-id");
    const userId = userIdText.innerText

    var send_data = [
        {"friendId": friendId},
        {"userId": userId}
      ];

    $.ajax({
        type: "POST",
        url: "/getFriend/",
        data: JSON.stringify(send_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            setFriend(result)
          } 
    });
}

function setFriend(result) {
    const friendButton = document.getElementById("friend-button");

    // check if is friend
    if (result.friend) {
        friendButton.innerText = "Un-Friend"
    } else {
        friendButton.innerText = "Friend"
    }
}