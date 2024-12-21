from django.urls import path

from task_manager.labels.views import (
    LabelFormCreateView,
    LabelFormDeleteView,
    LabelFormUpdateView,
    LabelsListView,
)

urlpatterns = [
    path("", LabelsListView.as_view(), name="labels_list"),
    path("create/", LabelFormCreateView.as_view(), name="create_label"),
    path(
        "<int:id>/update/", LabelFormUpdateView.as_view(), name="update_label"
    ),
    path(
        "<int:id>/delete/", LabelFormDeleteView.as_view(), name="delete_label"
    ),
]
