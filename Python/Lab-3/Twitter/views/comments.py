from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from Twitter.models import Comment
from ..forms import CommentForm
from ..managers import set_load_link


def render_comment(request, comment):
    return {
        "data": render_to_string(
            request=request,
            template_name='list_templates/comment.html',
            context={'comment': comment}
        )
    }


def comments_renderer(request, comments):
    rendered_comments = []
    for i in comments:
        rendered_comments.append(render_to_string(
            request=request,
            template_name='list_templates/comment.html',
            context={'comment': i}
        ))

    return rendered_comments


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def create_comment(request, twit_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment(user=auth.get_user(request), content=form.cleaned_data['content'], tweet_id=twit_id)
        comment.save()

        return JsonResponse(render_comment(request, comment))

    return HttpResponse(status=400)


@require_http_methods(['GET'])
def get_comments(request, twit_id, start_from_id, take):
    comments = Comment.objects.get_comments(request.user, take, start_from_id, tweet_id=twit_id)
    set_load_link(comments, take, 'comment/get', 'data-list')

    return JsonResponse({"data": comments_renderer(request, comments)})


@require_http_methods(['GET'])
def get_user_comments(request, take, start_from_id, user_id):
    comments = Comment.objects.get_comments(request.user, take, start_from_id, user_id=user_id)
    set_load_link(comments, take, 'comment/get', 'user-comments', user_id)

    return JsonResponse({"data": comments_renderer(request, comments)})
