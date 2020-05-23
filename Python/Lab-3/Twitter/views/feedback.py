import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from Twitter.models import Tweet, Comment, Like


@login_required()
@require_http_methods(["POST"])
def like_view(request, id):
    body = json.loads(request.body)

    if body['model'] == 'twit':
        obj = Tweet.objects.get(id=id)
    elif body['model'] == 'comment':
        obj = Comment.objects.get(id=id)
    else:
        return HttpResponse(status=400)

    like = Like.objects.is_like_exist(obj, request.user)
    if like is None:
        obj.likes.create(user=request.user)
        exist = True
    else:
        like.delete()
        exist = False

    return JsonResponse(
        {
            "like_count": obj.likes.count(),
            "exist": exist
        }
    )
