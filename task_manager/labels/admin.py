from django.contrib import admin

from task_manager.labels.models import Label


class LabelAdmin(admin.ModelAdmin[Label]):
    search_fields = ["name"]


admin.site.register(Label)
