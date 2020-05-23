$(document).on('submit', '#search-form', function (event) {
    event.preventDefault();

    let form = $('#search-form');
    let textareaVal = $('#textarea').val()
    let url = textareaVal.charAt(0) === '@' ? form[0].dataset.byusername : form[0].dataset.byname
    $.ajax({
        method: 'GET',
        url: window.location.origin  + url,
        data: form.serialize(),

        success: function (json) {
            $('#data-list').empty()
            prependData(json.data)
        }
    })
})