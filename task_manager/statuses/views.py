from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views import View
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.views import UserLoginRequiredMixin


class StatusesListView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        statuses = Status.objects.all()
        return render(
            request,
            "statuses_list.html",
            context={
                "statuses": statuses,
            },
        )


class StatusFormCreateView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = StatusForm()
        return render(request, "create_status.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            message = _("Status created successfully.")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("statuses_list")
        return render(request, "create_status.html", {"form": form})


class StatusFormUpdateView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, pk=status_id)
        form = StatusForm(instance=status)
        context = {"form": form, "status_id": status_id}
        return render(request, "update_status.html", context=context)

    def post(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, pk=status_id)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            message = _("Status has been updated successfully")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("statuses_list")
        context = {"form": form, "status_id": status_id}
        return render(request, "update_status.html", context=context)


class StatusFormDeleteView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, pk=status_id)
        return render(request, "delete_status.html", {"status": status})

    def post(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, pk=status_id)
        tasks_with_this_status = Task.objects.filter(status=status)
        if tasks_with_this_status:
            message = _("It is not possible to delete the status because it is in use")
            messages.add_message(request, messages.ERROR, message)
        else:
            status.delete()
            message = _("Status has been deleted successfully")
            messages.add_message(request, messages.SUCCESS, message)
        return redirect("statuses_list")
