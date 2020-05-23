$(window).scroll(function () {
    loadByMark();
});


function loadByMark() {
    const commonMark = 'end-mark-';
    let mark = $(`*[id*=${commonMark}]`);
    console.log('load')
    if (mark.is(':visible')) {
        console.log('asd')
        loadData(mark[0].dataset.link, mark[0].id.replace(commonMark, ''));
        mark.remove();
    }
}

function loadData(link, insertTo) {
    console.log(insertTo)
    fetch(window.location.origin + link, {
        method: 'GET',
        headers: getFetchHeader()
    })
    .then(response => response.json())
    .then(json => {
        $('#' + insertTo).append(json.data)
        setTargets()
    })
}
