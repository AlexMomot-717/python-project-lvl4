from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views import View


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "index.html")


class LoginServiceUserView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            message = _("You are signed in")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("index")
        else:
            message = _(
                "Please enter the correct username and password."
                " Both fields are case sensitive."
            )
            messages.add_message(request, messages.WARNING, message)
            form_data = {"username": username}
            return render(request, "login.html", context=form_data)


class LogoutServiceUserView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        message = _("You are signed out")
        messages.add_message(request, messages.INFO, message)
        return redirect("index")
