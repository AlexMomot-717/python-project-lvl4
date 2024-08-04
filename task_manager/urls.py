from django.contrib import admin
from django.urls import include, path
from task_manager import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginServiceUserView.as_view(), name="login"),
    path("logout/", views.LogoutServiceUserView.as_view(), name="logout"),
    path("users/", include("task_manager.users.urls")),
    path("statuses/", include("task_manager.statuses.urls")),
    path("admin/", admin.site.urls),
]
