from django.urls import path
from task_manager.users.views import (
    UserFormCreateView,
    UserFormDeleteView,
    UserFormEditView,
    UserListView,
)

urlpatterns = [
    path("", UserListView.as_view(), name="users_list"),
    path("create/", UserFormCreateView.as_view(), name="create_user"),
    path("<int:id>/edit/", UserFormEditView.as_view(), name="update_user"),
    path("<int:id>/delete/", UserFormDeleteView.as_view(), name="delete_user"),
]
