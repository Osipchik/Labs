from django.contrib import auth
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .. import forms


def signup_view(request):
    form = forms.UserCreateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.first_name = form.data['first_name']
            user.save()

            login(request, user)
            return redirect('home')

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    form = forms.AuthenticateForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')

    return render(request, 'accounts/login.html', context={'form': form})


@login_required(login_url='/accounts/login/')
@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('home')


@require_http_methods(['POST'])
@login_required(login_url='/accounts/login/')
def delete_account(request):
    user = auth.get_user(request)
    user.delete()
    return render(request, 'pages/extends/home.html')
