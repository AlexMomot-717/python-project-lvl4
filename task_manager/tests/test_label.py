import pytest
from django.forms.models import model_to_dict
from django.template.response import TemplateResponse
from django.test import Client
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.tests.helpers import (
    create_label,
    create_service_user,
    create_task,
)

pytestmark = pytest.mark.django_db


def test_labels_list(client: Client) -> None:
    # given
    create_label()
    service_user = create_service_user()
    client.force_login(service_user)
    labels = Label.objects.all()
    route = "/labels/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    context = {"csrf_token": csrf_token, "labels": labels}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "labels_list.html", context=context
    ).render()
    assert expected_html.content.decode() == response.content.decode()
    assert response.status_code == 200


def test_create_label_get(client: Client) -> None:
    # given
    create_label()
    service_user = create_service_user()
    client.force_login(service_user)
    route = "/labels/create/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    form = LabelForm()
    context = {"form": form, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "create_label.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_create_label_post(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    route = "/labels/create/"
    form_data = {
        "name": "bug",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    label_expected_dict = {"id": 1, "name": "bug"}
    assert model_to_dict(Label.objects.get()) == label_expected_dict
    assert response["Location"] == "/labels/"


def test_create_label_with_existing_name_post(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    create_label(name="bug")
    route = "/labels/create/"
    form_data = {
        "name": "bug",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert Label.objects.count() == 1
    assert "create_label.html" in [temp.name for temp in response.templates]


def test_update_label_get(client: Client) -> None:
    # given
    label = create_label()
    service_user = create_service_user()
    client.force_login(service_user)
    label_id = label.id
    route = f"/labels/{label_id}/update/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    form = LabelForm(instance=label)
    context = {"form": form, "label_id": label_id, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "update_label.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_update_label_does_not_exist(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    label_id = 1
    route = f"/labels/{label_id}/update/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


def test_update_label_post(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    label = create_label()
    label_id = label.id
    route = f"/labels/{label_id}/update/"
    form_data = {"name": "question"}

    # when
    response = client.post(route, data=form_data)

    # then
    assert Label.objects.get().name == "question"
    assert response["Location"] == "/labels/"


def test_update_label_post_form_is_not_valid(client: Client) -> None:
    # given
    label = create_label()
    service_user = create_service_user()
    client.force_login(service_user)
    label_id = label.id
    route = f"/labels/{label_id}/update/"
    form_data = {
        "name": "",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert Label.objects.get().name == "enhancement"
    assert response.status_code == 200


def test_delete_label(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    label = create_label()
    label_id = label.id
    route = f"/labels/{label_id}/delete/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    context = {"label": label, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "delete_label.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_delete_label_does_not_exist(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    label_id = 1
    route = f"/labels/{label_id}/delete/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


def test_delete_label_post_label_in_use(client: Client) -> None:
    # given
    task = create_task()
    service_user = task.author
    label = create_label()
    client.force_login(service_user)
    task.labels.add(label)
    label_id = label.id
    route = f"/labels/{label_id}/delete/"

    # when
    response = client.post(route)

    # then
    assert Label.objects.count() == 1
    assert response["Location"] == "/labels/"


def test_delete_label_post(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    label = create_label()
    label_id = label.id
    route = f"/labels/{label_id}/delete/"

    # when
    response = client.post(route)

    # then
    assert Label.objects.count() == 0
    assert response["Location"] == "/labels/"
