from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from Twitter.managers import set_load_link, get_objects_or_none, get_objects
from Twitter.models import Tweet
from accounts import forms
from accounts.models import UserProfile, Contact


def get_user(user_id):
    return User.objects.get(id=user_id)


@login_required(login_url='/accounts/login/')
@require_http_methods(["GET"])
def profile_view(request, id):
    user_profile = get_objects_or_none(User, id=id)[0]

    take = 10
    twits = user_profile.twits.get_user_twits(request.user, take, 0, id)
    set_load_link(twits, take, 'twit/get', 'user-twits', id)

    context = {
        'profile': user_profile,
        'twits': twits,
        'twits_count': user_profile.twits.count(),
        'description': forms.DescriptionForm(instance=UserProfile)
    }

    if request.is_ajax():
        return JsonResponse({
            "result": True,
            "main": render_to_string(
                request=request,
                template_name='pages/profile/profile.html',
                context=context
            )
        })

    return render(request, 'pages/extends/profile.html', context)


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def follow_view(request, author_id):
    user = get_objects_or_none(User, id=author_id)[0]
    if user and not Contact.objects.filter(user_from_id=request.user.id, user_to_id=author_id).exists():
        Contact.objects.create(
            user_from=request.user,
            user_to=user
        )
        return HttpResponse(status=201)

    return HttpResponse(status=404)


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def unfollow_view(request, author_id):
    contact = get_objects_or_none(Contact, user_from_id=request.user.id, user_to_id=author_id)
    if contact:
        contact.delete()
        return HttpResponse(status=201)

    return HttpResponse(status=404)
