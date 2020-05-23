from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from accounts import forms
from accounts.forms import DescriptionForm


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def update_user_image(request, image_type):
    form = forms.ImageForm(request.POST, request.FILES)
    if form.is_valid():
        profile = request.user.user_profile
        if image_type == 'image':
            profile.image = request.FILES['image']
        else:
            profile.header_image = request.FILES['image']

        profile.save()

        return HttpResponse(status=201)

    return HttpResponse(status=400)


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def change_description(request):
    form = DescriptionForm(request.POST)
    if form.is_valid():
        profile = request.user.user_profile
        profile.description = form.cleaned_data['description']
        profile.save()

        return HttpResponse(status=201)

    return HttpResponse(status=400)
