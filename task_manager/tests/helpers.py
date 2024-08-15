from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import ServiceUser


def create_service_user() -> ServiceUser:
    return ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )


def create_status() -> Status:
    return Status.objects.create(name="active")


def create_task() -> Task:
    service_user = create_service_user()
    status = create_status()
    return Task.objects.create(name="deploy", status=status, author=service_user)
