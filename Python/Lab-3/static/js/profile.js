var description_p = $('#description');
var descriptionInput = $('#change-description')[0].getElementsByTagName('textarea')[0];

$(document).ready(function () {
    descriptionInput.value = description_p.text();
    setTargets()
});

var headerImage = 'header-image';

var profileImages = {
    'image': $('#profile-image').find('img')[0],
    'header-image': $('#profile-header').find('img')[0],
};

var defaultImages = {
    'image': '/media/userpick.webp',
    'header-image': ''
};

var existingImages = {
    'image': profileImages["image"].src,
    'header-image': profileImages[headerImage].src,

};

function onpProfileImageChanged(event) {
    event.preventDefault();

    let files = event.target.files;
    if (files.length !== 0){
        profileImages[getImageId(event.target.id)].src = URL.createObjectURL(files[0]);
    }
}

function getImageId(id) {
    return id.replace('-input', '');
}

function deleteUserImage(event) {
    event.preventDefault();
    let imageId = getImageId(event.target.dataset.id);
    profileImages[imageId].src = existingImages[imageId] !== profileImages[imageId].src
        ? existingImages[imageId] : defaultImages[imageId];
}

function SubmitChanges(event) {
    event.preventDefault();

    submitFiles()

    description_p.text(descriptionInput.value)
    $.ajax({
        method: 'POST',
        url: window.location.origin + '/accounts/profile/personalize/change-description',
        data: $('#update-description').serialize(),
    })
}

function submitFiles() {
     let maxFileSize = 5242880;

    $('input[type=file]').each(async function () {

        // let data = new FormData();
        // data.append('image', this);

        if(this.files.length !== 0){
            if (this.files[0].size <= maxFileSize){
                let file = this.files[0];
                await uploadImages(file, this.dataset.url);
                if (this.id === 'image') {
                    $('.user-icon').each(function () {
                        this.src = URL.createObjectURL(file);
                    })
                }
                else if (this.id === headerImage) {
                    $('.profile-image-header').each(function () {
                        this.src = URL.createObjectURL(file);
                        this.removeClass('hide');
                    })
                }
            }
        }
        else {
            toggleAlert();
        }
    })
}

function toggleAlert(){
    $(".alert").toggleClass('in out');
    setTimeout(function () {
    }, 1000)
}

async function uploadImages(file, url) {
    let data = new FormData()
    data.append('image', file)
    try {
        const response = await fetch(window.location.origin + url, {
            method: 'POST',
            headers: getFetchHeader(),
            body: data
        });
        if (response.ok){

        }
    }
    catch (error) {
        console.error('Ошибка:', error);
    }
}