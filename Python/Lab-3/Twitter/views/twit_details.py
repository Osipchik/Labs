from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from Twitter import forms
from Twitter.managers import get_objects_or_none, set_load_link
from Twitter.models import Tweet, Comment


def twit_details(request, twit_id):
    take = 10
    twit = get_objects_or_none(Tweet, id=twit_id)[0]
    if request.user.is_authenticated:
        twit.is_liked = bool(twit.likes.is_like_exist(twit, request.user.id))

    comments = Comment.objects.get_comments(request.user, take, 0, tweet_id=twit_id)

    set_load_link(comments, take, 'comment/get/{}'.format(twit_id), 'data-list')
    context = {
        'form': forms.CommentForm(),
        'comments': comments,
        'twit': twit,
        'url': 'twit/comments/create/{}'.format(twit_id)
    }

    if request.is_ajax():
        return JsonResponse({
            "main": render_to_string(
                request=request,
                template_name='pages/twit_detail.html',
                context=context
            )
        })

    return render(request, 'pages/extends/twit_detail.html', context)
