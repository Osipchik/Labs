$('#exampleModal').modal({
  show: true
})

$(window).scroll(function () {
    setHeader();
});

function setHeader() {
    if ($(this).scrollTop() > 0){
        $("#head").addClass("default");
        $("#first-line").addClass("mt-h");
    }
    else {
        $("#head").removeClass("default");
        $("#first-line").removeClass("mt-h");
    }
}


const headScrollTop = () => {
    $('html,body').animate({ scrollTop: 0 }, 'slow');
}

async function link_clickHandler(event) {
    if (event.target.tagName !== 'I'){
        event.preventDefault();
        let path = (event.path || (event.composedPath && event.composedPath()) || event.target);
        let link = path.find(i => i.dataset !== undefined && 'ajaxlink' in i.dataset).dataset.ajaxlink;
        if (link !== window.location.pathname){
            await FetchMain(link);
        }
        else {
            headScrollTop();
        }
    }
}

async function FetchMain(link) {
    link = link.replace(window.location.origin  , '');

    let url = window.location.origin + (link[0] === '/' ? link : '/' + link);
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    if (response.ok){
        let res = await response.json();
        window.history.pushState({'url': url}, '', url);
        $("#main").replaceWith(res.main);
        setTargets();
    }
}

$(window).bind('popstate', async function(event) {
    let state = event.originalEvent.state;
    if(state) {
        await FetchMain(state.url);
    }
})

function prependData(data) {
    $('#data-list').prepend(data)
    setTargets();
}

function sendForm(event) {
    event.preventDefault();

    if ($('#textarea').val() === ''){
        return false
    }

    let form = $('#data-post')[0]
    $.ajax({
        method: 'POST',
        url: window.location.origin + '/' + form.dataset.url,
        data: new FormData(form),

        success: function (json) {
            form.reset()
            $('#tweet-image-container').remove()
            prependData(json.data)
        },

        cache: false,
        contentType: false,
        processData: false
    })
}