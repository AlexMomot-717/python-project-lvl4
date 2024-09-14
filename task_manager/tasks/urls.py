from tempfile import template

from django.urls import path
from django_filters.views import FilterView

from task_manager.tasks.models import Task
from task_manager.tasks.views import (
    TaskDetailsView,
    TaskFormCreateView,
    TaskFormDeleteView,
    TaskFormUpdateView,
    TaskListView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="tasks_list"),
    # path("", FilterView.as_view(model=Task), name="tasks_list"),
    path("<int:id>/", TaskDetailsView.as_view(), name="task_details"),
    path("create/", TaskFormCreateView.as_view(), name="create_task"),
    path("<int:id>/update/", TaskFormUpdateView.as_view(), name="update_task"),
    path("<int:id>/delete/", TaskFormDeleteView.as_view(), name="delete_task"),
]
