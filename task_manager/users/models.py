from django.contrib.auth.models import AbstractUser


class ServiceUser(AbstractUser):
    def __str__(self) -> str:
        return self.get_full_name()
