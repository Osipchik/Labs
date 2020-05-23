from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from Twitter.managers import get_objects_or_none, set_load_link
from accounts.models import Contact


@require_http_methods(["GET"])
def followers(request, user_id):
    user = get_objects_or_none(User, id=user_id)[0]
    user_followers = user.followers.all()

    context = {
        'data': user_followers,
    }

    if request.is_ajax():
        return JsonResponse({
            "main": render_to_string(
                request=request,
                template_name='pages/followers.html',
                context=context
            )
        })

    return render(request, 'pages/extends/followers.html', context)


@require_http_methods(["GET"])
def following(request, user_id):
    user = get_objects_or_none(User, id=user_id)[0]
    user_following = user.following.all()

    context = {
        'data': user_following,
    }

    if request.is_ajax():
        return JsonResponse({
            "main": render_to_string(
                request=request,
                template_name='pages/following.html',
                context=context
            )
        })

    return render(request, 'pages/extends/following.html', context)

