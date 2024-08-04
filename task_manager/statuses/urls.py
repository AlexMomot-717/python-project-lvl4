from django.urls import path
from task_manager.statuses.views import (
    StatusesListView,
    StatusFormCreateView,
    StatusFormDeleteView,
    StatusFormEditView,
)

urlpatterns = [
    path("", StatusesListView.as_view(), name="statuses_list"),
    path("create/", StatusFormCreateView.as_view(), name="create_status"),
    path("<int:id>/edit/", StatusFormEditView.as_view(), name="update_status"),
    path("<int:id>/delete/", StatusFormDeleteView.as_view(), name="delete_status"),
]
