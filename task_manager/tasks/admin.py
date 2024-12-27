from django.contrib import admin

from task_manager.tasks.models import Task


class TaskAdmin(admin.ModelAdmin[Task]):
    search_fields = ["executor", "status"]


admin.site.register(Task)
