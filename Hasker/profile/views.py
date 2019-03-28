from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from Hasker.profile.forms import HaskerUserSettingsForm, HaskerUserForm
from Hasker.hasker.views import base
from Hasker.httpcodes import *

User = get_user_model()


def login_view(request):
    context = base(request)
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mainpage')
        else:
            context.update({'login_failed': True})
            return render(request, 'login.html', context, status=HTTP_UNAUTHORIZED)
    else:
        return render(request, "login.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('mainpage')


def signup_view(request):
    context = base(request)
    context.update({'form': HaskerUserForm})
    status = HTTP_OK
    if request.method == "POST":
        user_form = HaskerUserForm(request.POST, request.FILES)

        context.update({'form': user_form})
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            context.update({'user': user})
            login(request, user)
            return render(request, 'signup_complete.html', context)
        else:
            status = HTTP_BAD_REQUEST

    return render(request, 'signup.html', context, status=status)


@login_required
def settings_view(request):
    context = base(request)
    user = context["user"]
    context.update({"form": HaskerUserSettingsForm})
    status = HTTP_OK
    if request.method == "POST":
        user_settings_form = HaskerUserSettingsForm(request.POST, request.FILES, instance=user)
        context.update({'form': user_settings_form})
        if user_settings_form.is_valid():
            user_update = user_settings_form.save(commit=False)
            user_update.set_password(user_update.password)
            user_update.save()
            context.update({'user': user_update})
        else:
            status = HTTP_BAD_REQUEST

    return render(request, 'settings.html', context, status=status)
