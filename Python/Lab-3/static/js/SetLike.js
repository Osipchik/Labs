function setLike(event) {
    let like = event.path.find(i => i.dataset !== undefined && 'like' in i.dataset);
    let likeCount = like.getElementsByTagName('small')[0]

    $.ajax({
        url: "/like/" + like.dataset.id + "/",
        type: 'POST',
        headers: {
            "Accept": "application/json; odata=verbose"
        },
        data: JSON.stringify({'model': like.dataset.like}),

        success: function (json) {

            if (json.like_count){
                likeCount.innerHTML = json.like_count
            }

            let icon = like.querySelector("[data-icon=like]")

            if (json.exist === true) {
                like.classList.add("text-red");
                icon.classList.remove("far");
                icon.classList.add("fas");
            } else {
                like.classList.remove("text-red");
                icon.classList.remove("fas");
                icon.classList.add("far");
            }
        }
    });
}
