 function addBookmark(event, twitId, url) {
    event.preventDefault();

    fetch(window.location.origin + url, {
        method: 'POST',
        headers: getFetchHeader()
    })
    .then(response => response.json())
    .then(json => changeTwit(json.data, twitId));
}

function removeBookmark(event, twitId, url) {
    event.preventDefault();

    fetch(window.location.origin + url, {
        method: 'DELETE',
        headers: getFetchHeader()
    })
    .then(response => response.json())
    .then(json => changeTwit(json.data, twitId));
}