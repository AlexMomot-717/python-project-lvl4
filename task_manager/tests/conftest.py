from typing import Generator

import pytest
from django.test import Client
from freezegun import freeze_time
from task_manager.users.models import ServiceUser


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def service_user() -> ServiceUser:
    return ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )


@pytest.fixture(autouse=True, scope="session")
def fix_datetime() -> Generator[None, None, None]:
    with freeze_time("15.07.2024 17:00"):
        yield
