from typing import Generator

import pytest
from django.test import Client
from freezegun import freeze_time


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture(autouse=True, scope="session")
def fix_datetime() -> Generator[None, None, None]:
    with freeze_time("15.07.2024 17:00"):
        yield
