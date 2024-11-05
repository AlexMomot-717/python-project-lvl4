from django.contrib import admin

from task_manager.users.models import ServiceUser


class ServiceUserAdmin(admin.ModelAdmin[ServiceUser]):
    search_fields = ["username"]


admin.site.register(ServiceUser)
