function followFetch(url, text, addClass, removeClass, action) {
    fetch(window.location.origin + url, {
        method: 'POST',
        headers: getFetchHeader()
    })
    .then(response => {
        if (response.ok){
            let btn = $('#follow-btn')[0]
            btn.dataset.action = action;
            $(btn).removeClass(removeClass);
            $(btn).addClass(addClass);
            $(btn).text(text);
        }
    })
}

function followBtnClickHandler(event) {
    const follow = ['follow', 'Читать', 'hover-blue'];
    const unfollow = ['unfollow', 'Перестать читать', 'hover-red'];
    if (event.target.dataset.action === follow[0]){
        followFetch(event.target.dataset.followurl, unfollow[1], unfollow[2], follow[2], unfollow[0])
    }
    else{
        followFetch(event.target.dataset.unfollowurl, follow[1], follow[2], unfollow[2], follow[0])
    }
}

async function unfollow(url) {
    console.log(url)
    let response = await fetch(window.location.origin + url,{
        method: 'POST',
        headers: getFetchHeader()
    })
    if (response.ok){
        console.log('ok')
    }
}