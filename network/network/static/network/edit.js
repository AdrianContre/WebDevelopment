function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) {
        return parts.pop().split(';').shift();
    }
}

//this function enables us to manipulate the edit post event
function handleEdit(postId) {
    const newValue = document.getElementById(`textarea_${postId}`).value;
    const postText = document.getElementById(`text_${postId}`);
    const modal = document.getElementById(`modal_editPost_${postId}`);
    //as we already have the value, we have to send to the backend
    fetch(`/editPost/${postId}`,{
        method: 'POST',
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: newValue
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        postText.innerHTML = result["newContent"]
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden','true');
        modal.setAttribute('style','display: none');
        const modalBackdrop = document.getElementsByClassName('modal-backdrop');
        for (let i = 0; i < modalBackdrop.length; ++i) {
            document.body.removeChild(modalBackdrop[i]);
        document.body.style.overflow = 'auto'; // Reactivar scroll en el body
        }

    });
}