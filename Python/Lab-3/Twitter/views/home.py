from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .. import forms
from ..managers import set_load_link
from ..models import Tweet


def home(request):

    take = 10
    twits = Tweet.objects.get_twits(request.user, take, 0)
    set_load_link(twits, take, 'twit/get', 'data-list')
    context = {'form': forms.CreateTwit(), 'twits': twits, 'url': 'twit/create/'}

    if request.is_ajax():
        return JsonResponse({
            "result": True,
            "main": render_to_string(
                request=request,
                template_name='pages/home.html',
                context=context
            )
        })

    return render(request, 'pages/extends/home.html', context)
