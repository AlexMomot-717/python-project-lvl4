from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views import View

from task_manager.settings import LOGIN_URL
from task_manager.tasks.models import Task
from task_manager.users.forms import ServiceUserForm
from task_manager.users.models import ServiceUser


class UserLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: str | int
    ) -> Any:
        if not request.user.is_authenticated:
            message = _("You are not authorized! Please sign in.")
            messages.add_message(request, messages.ERROR, message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        users = ServiceUser.objects.all()
        return render(
            request,
            "users_list.html",
            context={
                "users": users,
            },
        )


class UserFormCreateView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = ServiceUserForm()
        return render(request, "create_user.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        user_form = ServiceUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            message = _("User signed up successfully.")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect(LOGIN_URL)
        return render(request, "create_user.html", {"form": user_form})


class UserFormUpdateView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        user_id = kwargs.get("id")
        user = get_object_or_404(ServiceUser, pk=user_id)
        if request.user != user:
            message = _(
                "You do not have permission to update or delete another user."
            )
            messages.add_message(request, messages.ERROR, message)
            return redirect("users_list")
        form = ServiceUserForm(instance=user)
        context = {"form": form, "user_id": user_id}
        return render(request, "update_user.html", context=context)

    def post(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        user_id = kwargs.get("id")
        user = get_object_or_404(ServiceUser, pk=user_id)
        user_form = ServiceUserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            message = _("User has been updated successfully")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("users_list")
        context = {"form": user_form, "user_id": user_id}
        return render(request, "update_user.html", context=context)


class UserFormDeleteView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        user_id = kwargs.get("id")
        user = get_object_or_404(ServiceUser, pk=user_id)
        if request.user != user:
            message = _(
                "You do not have permission to update or delete another user."
            )
            messages.add_message(request, messages.ERROR, message)
            return redirect("users_list")
        return render(request, "delete_user.html", {"user": user})

    def post(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        user_id = kwargs.get("id")
        user = get_object_or_404(ServiceUser, pk=user_id)
        tasks_where_user_is_author = Task.objects.filter(author=user)
        tasks_where_user_is_executor = Task.objects.filter(executor=user)
        if tasks_where_user_is_author or tasks_where_user_is_executor:
            message = _(
                "It is not possible to delete the user because it is used"
            )
            messages.add_message(request, messages.ERROR, message)
        else:
            user.delete()
            message = _("User has been deleted successfully")
            messages.add_message(request, messages.SUCCESS, message)
        return redirect("users_list")
