from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views import View
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.users.models import ServiceUser
from task_manager.users.views import UserLoginRequiredMixin


class TaskListView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        tasks = Task.objects.all()
        return render(
            request,
            "tasks_list.html",
            context={
                "tasks": tasks,
            },
        )


class TaskDetailsView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        task_id = kwargs.get("id")
        task = get_object_or_404(Task, pk=task_id)
        return render(
            request,
            "task_details.html",
            context={
                "task": task,
            },
        )


class TaskFormCreateView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = TaskForm()
        return render(request, "create_task.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = TaskForm(request.POST)
        if form.is_valid() and isinstance(request.user, ServiceUser):
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            status = form.cleaned_data["status"]
            author = request.user
            executor = form.cleaned_data["executor"]
            Task.objects.create(
                name=name,
                description=description,
                status=status,
                author=author,
                executor=executor,
            )
            message = _("Task created successfully.")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("tasks_list")
        return render(request, "create_task.html", {"form": form})


class TaskFormUpdateView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        task_id = kwargs.get("id")
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        context = {"form": form, "task_id": task_id}
        return render(request, "update_task.html", context=context)

    def post(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        task_id = kwargs.get("id")
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            message = _("Task has been updated successfully")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("tasks_list")
        context = {"form": form, "task_id": task_id}
        return render(request, "update_task.html", context=context)


class TaskFormDeleteView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        task_id = kwargs.get("id")
        task = get_object_or_404(Task, pk=task_id)
        if request.user != task.author:
            message = _("Only task author can delete it.")
            messages.add_message(request, messages.ERROR, message)
            return redirect("tasks_list")
        return render(request, "delete_task.html", {"task": task})

    def post(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        task_id = kwargs.get("id")
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        message = _("Task has been deleted successfully")
        messages.add_message(request, messages.SUCCESS, message)
        return redirect("tasks_list")
