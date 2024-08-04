import pytest
from django.template.response import TemplateResponse
from django.test import Client
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.users.models import ServiceUser

pytestmark = pytest.mark.django_db


def test_statuses_list(client: Client, service_user: ServiceUser) -> None:
    # given
    client.force_login(service_user)
    Status.objects.create(name="frozen")
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


def test_create_status_get(client: Client, service_user: ServiceUser) -> None:
    # given
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


def test_create_status_post(client: Client, service_user: ServiceUser) -> None:
    # given
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


def test_edit_status_get(client: Client, service_user: ServiceUser) -> None:
    # given
    status = Status.objects.create(name="frozen")

    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/edit/"

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


def test_edit_status_does_not_exist(client: Client, service_user: ServiceUser) -> None:
    # given
    client.force_login(service_user)
    status_id = 1
    route = f"/statuses/{status_id}/edit/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


def test_edit_status_post(client: Client, service_user: ServiceUser) -> None:
    # given
    status = Status.objects.create(name="frozen")
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/edit/"
    form_data = {
        "name": "reopened",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert Status.objects.get(id=status_id).name == "reopened"
    assert response["Location"] == "/statuses/"


def test_edit_status_post_form_is_not_valid(
    client: Client, service_user: ServiceUser
) -> None:
    # given
    status = Status.objects.create(name="frozen")
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/edit/"
    form_data = {
        "name": "",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert Status.objects.get(id=1) == status
    assert response.status_code == 200


def test_delete_status(client: Client, service_user: ServiceUser) -> None:
    # given
    status = Status.objects.create(name="frozen")
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


def test_delete_status_does_not_exist(
    client: Client, service_user: ServiceUser
) -> None:
    # given
    client.force_login(service_user)
    status_id = 1
    route = f"/statuses/{status_id}/delete/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


def test_delete_status_post(client: Client, service_user: ServiceUser) -> None:
    # given
    status = Status.objects.create(name="frozen")
    client.force_login(service_user)
    status_id = status.id
    route = f"/statuses/{status_id}/delete/"

    # when
    response = client.post(route)

    # then
    assert Status.objects.count() == 0
    assert response["Location"] == "/statuses/"
