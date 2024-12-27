from django.urls import path

from task_manager.statuses.views import (
    StatusesListView,
    StatusFormCreateView,
    StatusFormDeleteView,
    StatusFormUpdateView,
)

urlpatterns = [
    path("", StatusesListView.as_view(), name="statuses_list"),
    path("create/", StatusFormCreateView.as_view(), name="create_status"),
    path(
        "<int:id>/update/", StatusFormUpdateView.as_view(), name="update_status"
    ),
    path(
        "<int:id>/delete/", StatusFormDeleteView.as_view(), name="delete_status"
    ),
]
