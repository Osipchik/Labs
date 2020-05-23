from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from Twitter.models import Tweet, Like
from ..forms import CreateTwit
from ..managers import get_objects_or_none, prepare_tweet, set_load_link


def render_twit(request, twit):
    return {
        "data": render_to_string(
            request=request,
            template_name='list_templates/twit/twit.html',
            context={'twit': twit}
        )
    }


def twits_renderer(request, twits):
    rendered_twits = []
    for i in twits:
        rendered_twits.append(render_to_string(
            request=request,
            template_name='list_templates/twit/twit.html',
            context={'twit': i}
        ))

    return rendered_twits


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def create_twit(request):
    form = CreateTwit(request.POST, request.FILES)
    if form.is_valid():
        twit = Tweet(user=auth.get_user(request),
                     content=form.cleaned_data['content'],
                     image=form.cleaned_data['image'])
        twit.save()
        twit.is_liked = False

        return JsonResponse(render_twit(request, twit))

    return HttpResponse(status=400)


@login_required(login_url='/accounts/login/')
@require_http_methods(["PATCH"])
def delete_twit(request, twit_id):
    twit = get_objects_or_none(Tweet, id=twit_id)[0]

    if twit is None:
        return Http404('twit with id: {} does not exist'.format(twit_id))
    elif not twit.is_deleted:
        twit.is_deleted = True
        twit.save()
    elif twit.is_deleted:
        twit.delete()
        return HttpResponse(status=201)

    prepare_tweet(twit, request.user.id)

    return JsonResponse(render_twit(request, twit))


@login_required(login_url='/accounts/login/')
@require_http_methods(["PATCH"])
def restore_twit(request, twit_id):
    twit = get_objects_or_none(Tweet, id=twit_id)[0]

    if twit is None:
        return Http404('twit with id: {} does not exist'.format(twit_id))

    twit.is_deleted = False
    twit.save()

    prepare_tweet(twit, request.user.id)

    return JsonResponse(render_twit(request, twit))


@require_http_methods(['GET'])
def get_twits(request, take, start_from_id):
    twits = Tweet.objects.get_twits(request.user, take, start_from_id)
    set_load_link(twits, take, 'twit/get', 'twits')

    return JsonResponse({"data": twits_renderer(request, twits)})


@require_http_methods(['GET'])
def get_user_twits(request, take, start_from_id, user_id):
    twits = Tweet.objects.get_user_twits(auth.get_user(request), take, start_from_id, user_id)
    set_load_link(twits, take, 'twit/get', 'user-twits', user_id)

    return JsonResponse({"data": twits_renderer(request, twits)})


@require_http_methods(['GET'])
def get_liked_twits(request, take, start_from_id, user_id):
    kwargs = {
        'content_type': ContentType.objects.get_for_model(Tweet),
        'user_id': user_id,
    }

    if start_from_id < 0:
        kwargs['object_id__lt'] = -start_from_id
    elif start_from_id > 0:
        kwargs['object_id__gt'] = start_from_id

    likes = get_objects_or_none(Like, **kwargs)

    if request.user.is_authenticated:
        twits = [prepare_tweet(i.content_object, request.user.id) for i in likes.order_by('-object_id')[:take]]
    else:
        twits = [i.content_object for i in likes.order_by('-object_id')[:take]]

    set_load_link(twits, take, 'twit/liked', 'liked-twits', user_id)

    return JsonResponse({"data": twits_renderer(request, twits)})


@require_http_methods(['GET'])
def get_media_twits(request, take, start_from_id, user_id):
    twits = Tweet.objects.get_user_twits(auth.get_user(request), take, start_from_id, user_id, image__isnull=False)
    set_load_link(twits, take, 'twit/media', 'user-media', user_id)

    return JsonResponse({"data": twits_renderer(request, twits)})