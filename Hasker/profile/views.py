from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from Hasker.profile.forms import HaskerUserSettingsForm, HaskerUserForm
from Hasker.helpers import base
from Hasker.profile.helpers import save_haskeruser_by_form, update_hasker_user_by_form
from Hasker.httpcodes import HTTP_BAD_REQUEST, HTTP_OK, HTTP_UNAUTHORIZED

HaskerUser = get_user_model()


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
        user = save_haskeruser_by_form(request, context)
        if user:
            login(request, user)
            return render(request, 'signup_complete.html', context)
        else:
            status = HTTP_BAD_REQUEST

    return render(request, 'signup.html', context, status=status)


@login_required
def settings_view(request):
    context = base(request)
    context.update({"form": HaskerUserSettingsForm})
    status = HTTP_OK
    if request.method == "POST":
        user = update_hasker_user_by_form(request, context)
        if not user:
            status = HTTP_BAD_REQUEST

    return render(request, 'settings.html', context, status=status)


def handler404(request, exception, template_name="404.html"):
    context = base(request)
    context.update({"ttt": "test"})
    response = render("404.html", context, status=404)
    return response


def handler500(request, exception, template_name="500.html"):
    context = base(request)
    response = render("500.html", context)
    response.status_code = 500
    return response
