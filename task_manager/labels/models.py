from django.db import models


class Label(models.Model):
    name = models.CharField(unique=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
