import pytest
from django.template.response import TemplateResponse
from django.test import Client
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.tests.helpers import (
    create_service_user,
    create_status,
    create_task,
)

pytestmark = pytest.mark.django_db


def test_statuses_list(client: Client) -> None:
    # given
    create_status()
    service_user = create_service_user()
    client.force_login(service_user)
    statuses = Status.objects.all()
    route = "/statuses/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    context = {"csrf_token": csrf_token, "statuses": statuses}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "statuses_list.html", context=context
    ).render()
    assert expected_html.content.decode() == response.content.decode()
    assert response.status_code == 200


def test_create_status_get(client: Client) -> None:
    # given
    create_status()
    service_user = create_service_user()
    client.force_login(service_user)
    route = "/statuses/create/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    form = StatusForm()
    context = {"form": form, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "create_status.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_create_status_post(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    route = "/statuses/create/"
    form_data = {
        "name": "reopened",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert Status.objects.get(id=1).name == "reopened"
    assert response["Location"] == "/statuses/"


def test_update_status_get(client: Client) -> None:
    # given
    status = create_status()
    service_user = create_service_user()
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/update/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    form = StatusForm(instance=status)
    context = {"form": form, "status_id": status_id, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "update_status.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_update_status_does_not_exist(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    status_id = 1
    route = f"/statuses/{status_id}/update/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


def test_update_status_post(client: Client) -> None:
    # given
    status = create_status()
    service_user = create_service_user()
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/update/"
    form_data = {
        "name": "reopened",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert Status.objects.get(id=status_id).name == "reopened"
    assert response["Location"] == "/statuses/"


def test_update_status_post_form_is_not_valid(client: Client) -> None:
    # given
    status = create_status()
    service_user = create_service_user()
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/update/"
    form_data = {
        "name": "",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert Status.objects.get(id=1) == status
    assert response.status_code == 200


def test_delete_status(client: Client) -> None:
    # given
    status = create_status()
    service_user = create_service_user()
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/delete/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    context = {"status": status, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "delete_status.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_delete_status_does_not_exist(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    status_id = 1
    route = f"/statuses/{status_id}/delete/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


def test_delete_status_post_status_in_use(client: Client) -> None:
    # given
    task = create_task()
    service_user = task.author
    status = task.status
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/delete/"

    # when
    response = client.post(route)

    # then
    assert Status.objects.count() == 1
    assert response["Location"] == "/statuses/"


def test_delete_status_post(client: Client) -> None:
    # given
    status = create_status()
    service_user = create_service_user()
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/delete/"

    # when
    response = client.post(route)

    # then
    assert Status.objects.count() == 0
    assert response["Location"] == "/statuses/"
