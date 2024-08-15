from django.db import models
from task_manager.statuses.models import Status
from task_manager.users.models import ServiceUser


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(
        ServiceUser, related_name="user_author", on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        ServiceUser,
        related_name="user_executor",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
