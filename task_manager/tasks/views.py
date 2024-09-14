from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views import View
from mypyc.doc.conf import author

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.users.models import ServiceUser
from task_manager.users.views import UserLoginRequiredMixin


class TaskListView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        # status = kwargs.get("status")
        # executor = kwargs.get("executor")
        # label = kwargs.get("label")
        # self_tasks = kwargs.get("self_tasks")
        # if self_tasks:
        #     author = request.user
        # else:
        #     author = None
        # if kwargs:
        #     task_filter = TaskFilter(request.GET, queryset=Task.objects.filter(status=status, author=author, executor=executor, label=label))
        # else:
        task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
        statuses = Status.objects.all()
        executors = ServiceUser.objects.all()
        author = request.user.id
        labels = Label.objects.all()
        return render(
            request,
            "tasks_list.html",
            context={
                "filter": task_filter,
                "statuses": statuses,
                "author": author,
                "executors": executors,
                "labels": labels
            }
        )


class TaskDetailsView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        task_id = kwargs.get("id")
        task = get_object_or_404(Task, pk=task_id)
        labels = get_object_or_404(Task, pk=task_id).labels.all()
        return render(
            request,
            "task_details.html",
            context={
                "task": task,
                "labels": labels,
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
            labels = form.cleaned_data["labels"]
            task = Task(
                name=name,
                description=description,
                status=status,
                author=author,
                executor=executor,
            )
            task.save()
            task.labels.add(*labels)
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
