from django.contrib import admin

from task_manager.statuses.models import Status


class StatusAdmin(admin.ModelAdmin[Status]):
    search_fields = ["name"]


admin.site.register(Status)
