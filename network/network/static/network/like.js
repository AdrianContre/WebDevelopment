function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) {
        return parts.pop().split(';').shift();
    }
}

function likeHandler(postId) {
    const button = document.getElementById(`button_like_${postId}`);
    const heart = document.getElementById(`heart_${postId}`);
    if (heart.classList.contains("far")) {
        heart.className = "fas fa-heart";
        updateLike(postId,"increase");
    } else {
        heart.className = "far fa-heart";
        updateLike(postId,"decrease");
    }
}

function updateLike(postId,action) {
    if (action === "increase") {
        fetch(`/increaseLike/${postId}`,{
            method: 'POST',
            headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")}
        })
        .then(response => response.json())
        .then(result => {
            const numberLikes = document.getElementById(`numberLikes_${postId}`);
            numberLikes.innerHTML = result["numberOfLikes"];
        })
    }
    else {
        fetch(`/decreaseLike/${postId}`,{
            method: 'POST',
            headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")}
        })
        .then(response => response.json())
        .then(result => {
            const numberLikes = document.getElementById(`numberLikes_${postId}`);
            numberLikes.innerHTML = result["numberOfLikes"];
        })
    }
}





