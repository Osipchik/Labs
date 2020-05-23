import asyncio

from channels.db import database_sync_to_async
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from .. import forms
from ..managers import set_load_link


@database_sync_to_async
def get_users(user, take, skip):
    users = User.objects.all()
    if user.is_authenticated:
        users = users.exclude(id=user.id)
    return users[skip:take]


def get_users_(user, **kwargs):
    users = User.objects.filter(**kwargs)
    if user.is_authenticated:
        users = users.exclude(id=user.id)
    return users


def search(request):
    form = forms.SearchForm()

    loop = asyncio.new_event_loop()
    users = loop.run_until_complete(get_users(auth.get_user(request), 10, 0))
    loop.close()

    context = {'form': form, 'users': users}

    if request.is_ajax():
        return JsonResponse({
            "main": render_to_string(
                request=request,
                template_name='pages/search.html',
                context=context
            )
        })

    return render(request, 'pages/extends/search.html', context)


def users_renderer(request, users):
    rendered_users = []
    for i in users:
        rendered_users.append(render_to_string(
            request=request,
            template_name='list_templates/user.html',
            context={'author': i}
        ))
    return rendered_users


@require_http_methods(["GET"])
def find_users_by_name(request):
    form = forms.SearchForm(request.GET)
    if form.is_valid():
        search_by = form.cleaned_data['content']
        users = get_users_(request.user, first_name__icontains=search_by)

        return JsonResponse({'data': users_renderer(request, users)})

    return HttpResponse(status=404)


@require_http_methods(["GET"])
def find_users_by_username(request):
    form = forms.SearchForm(request.GET)
    if form.is_valid():
        search_by = form.cleaned_data['content'][1:]
        users = get_users_(request.user, username__icontains=search_by)
        return JsonResponse({'data': users_renderer(request, users)})

    return HttpResponse(status=404)
