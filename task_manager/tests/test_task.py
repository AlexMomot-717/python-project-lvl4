import pytest
from django.forms.models import model_to_dict
from django.template.response import TemplateResponse
from django.test import Client
from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.tests.fixtures.expected_pieces_html import (
    EXPECTED_HTML_FILTERS_ARE_NOT_SET,
    EXPECTED_HTML_FILTERS_ARE_SET,
    EXPECTED_HTML_FILTERS_ARE_SET_EMPTY_QUERYSET,
    EXPECTED_HTML_FILTERS_ARE_SET_REQUEST_USER_TASKS_ONLY,
)
from task_manager.tests.helpers import (
    create_label,
    create_service_user,
    create_status,
    create_task,
)
from task_manager.users.models import ServiceUser

pytestmark = pytest.mark.django_db


def test_tasks_list(client: Client) -> None:
    # given
    task_1 = create_task()
    label_1 = create_label()
    label_2 = create_label(name="docs")
    task_1.labels.add(label_1, label_2)
    task_1.save()
    service_user_2 = create_service_user(
        first_name="taylor", last_name="swift", username="alison", password="*****"
    )
    status_2 = create_status(name="frozen")
    task_2 = Task.objects.create(
        name="fix", status=status_2, author=service_user_2, executor=task_1.author
    )
    task_2.labels.add(label_2)
    task_2.save()
    client.force_login(task_1.author)
    route = "/tasks/"

    # when
    response = client.get(route)

    # then
    expected_html_piece = EXPECTED_HTML_FILTERS_ARE_NOT_SET.format(task_1.id, task_2.id)
    assert expected_html_piece in response.content.decode()
    assert response.status_code == 200


def test_tasks_list_request_user_tasks_only(client: Client) -> None:
    # given
    task_1 = create_task()
    label_1 = create_label()
    label_2 = create_label(name="docs")
    task_1.labels.add(label_1, label_2)
    task_1.save()
    service_user_2 = create_service_user(
        first_name="taylor", last_name="swift", username="alison", password="*****"
    )
    status_2 = create_status(name="frozen")
    task_2 = Task.objects.create(
        name="fix", status=status_2, author=service_user_2, executor=task_1.author
    )
    task_2.labels.add(label_2)
    task_2.save()
    client.force_login(task_1.author)
    route = "/tasks/"

    # when
    response = client.get(route, query_params={"request_user_tasks": True})

    # then
    expected_html_piece = EXPECTED_HTML_FILTERS_ARE_SET_REQUEST_USER_TASKS_ONLY.format(
        task_1.id
    )
    assert expected_html_piece in response.content.decode()
    assert response.status_code == 200


def test_tasks_list_filters_are_set(client: Client) -> None:
    # given
    task_1 = create_task()
    label_1 = create_label()
    label_2 = create_label(name="docs")
    task_1.labels.add(label_1, label_2)
    task_1.save()
    service_user_2 = create_service_user(
        first_name="taylor", last_name="swift", username="alison", password="*****"
    )
    status_2 = create_status(name="frozen")
    task_2 = Task.objects.create(
        name="fix", status=status_2, author=service_user_2, executor=task_1.author
    )
    task_2.labels.add(label_2)
    task_2.save()
    client.force_login(task_1.author)
    route = "/tasks/"

    # when
    response = client.get(route, query_params={"status": status_2.id})

    # then
    expected_html_piece = EXPECTED_HTML_FILTERS_ARE_SET.format(task_2.id)
    assert expected_html_piece in response.content.decode()
    assert response.status_code == 200


def test_tasks_list_filters_are_set_empty_queryset(client: Client) -> None:
    # given
    task_1 = create_task()
    label_1 = create_label()
    label_2 = create_label(name="docs")
    label_3 = create_label(name="bug")
    task_1.labels.add(label_1, label_2)
    task_1.save()
    service_user_2 = create_service_user(
        first_name="taylor", last_name="swift", username="alison", password="*****"
    )
    status_2 = create_status(name="frozen")
    task_2 = Task.objects.create(
        name="fix", status=status_2, author=service_user_2, executor=task_1.author
    )
    task_2.labels.add(label_2)
    task_2.save()
    client.force_login(task_1.author)
    route = "/tasks/"

    # when
    response = client.get(
        route, query_params={"labels": label_3.id, "request_user_tasks": True}
    )

    # then
    expected_html_piece = EXPECTED_HTML_FILTERS_ARE_SET_EMPTY_QUERYSET
    assert expected_html_piece in response.content.decode()
    assert response.status_code == 200


def test_task_details(client: Client) -> None:
    # given
    task = create_task()
    client.force_login(task.author)
    route = f"/tasks/{task.id}/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    context = {"csrf_token": csrf_token, "task": task}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "task_details.html", context=context
    ).render()
    assert expected_html.content.decode() == response.content.decode()
    assert response.status_code == 200


def test_create_task_get(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    route = "/tasks/create/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    form = TaskForm()
    context = {"form": form, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "create_task.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_create_task_post(client: Client) -> None:
    # given
    status = create_status()
    service_user = create_service_user()
    label = create_label()
    client.force_login(service_user)
    route = "/tasks/create/"
    form_data = {
        "name": "fix",
        "description": "",
        "status": status.id,
        "executor": service_user.id,
        "labels": [label.id],
    }

    # when
    response = client.post(route, data=form_data)

    # then
    task = Task.objects.get()
    assert model_to_dict(task)["name"] == "fix"
    assert model_to_dict(task)["labels"] == [label]
    assert response["Location"] == "/tasks/"


def test_update_task_get(client: Client) -> None:
    # given
    task = create_task()
    client.force_login(task.author)
    route = f"/tasks/{task.id}/update/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    form = TaskForm(instance=task)
    context = {"form": form, "task_id": task.id, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "update_task.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_update_task_does_not_exist(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    task_id = 1
    route = f"/tasks/{task_id}/update/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


def test_update_task_post(client: Client) -> None:
    # given
    task = create_task()
    service_user = task.author
    status_new = Status.objects.create(name="frozen")
    label1 = create_label()
    label2 = create_label(name="issue#17")
    client.force_login(service_user)
    route = f"/tasks/{task.id}/update/"
    form_data = {
        "name": "fix",
        "description": "",
        "status": status_new.id,
        "executor": service_user.id,
        "labels": [label2.id, label1.id],
    }

    # when
    response = client.post(route, data=form_data)

    # then
    task = Task.objects.get()
    assert model_to_dict(task)["name"] == "fix"
    assert model_to_dict(task)["status"] == status_new.id
    assert model_to_dict(task)["labels"] == [label1, label2]
    assert response["Location"] == "/tasks/"


def test_update_task_post_form_is_not_valid(client: Client) -> None:
    # given
    task = create_task()
    service_user = task.author
    client.force_login(service_user)
    task_id = task.id
    route = f"/tasks/{task_id}/update/"
    form_data = {
        "name": "fix",
        "description": "",
        "author": service_user.id,
        "executor": service_user.id,
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert Task.objects.get().name == "deploy"
    assert response.status_code == 200
    assert "update_task.html" in [temp.name for temp in response.templates]


def test_delete_task(client: Client) -> None:
    # given
    task = create_task()
    client.force_login(task.author)
    task_id = task.id
    route = f"/tasks/{task_id}/delete/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    context = {"task": task, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "delete_task.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


def test_delete_task_does_not_exist(client: Client) -> None:
    # given
    service_user = create_service_user()
    client.force_login(service_user)
    task_id = 1
    route = f"/tasks/{task_id}/delete/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


def test_delete_task_request_user_is_not_author(client: Client) -> None:
    # given
    task = create_task()
    request_user = ServiceUser.objects.create(
        first_name="taylor", last_name="swift", username="alison", password="*****"
    )
    client.force_login(request_user)
    task_id = task.id
    route = f"/tasks/{task_id}/delete/"

    # when
    response = client.get(route)

    # then
    actual_task = Task.objects.get()
    assert actual_task == task
    assert Task.objects.count() == 1
    assert response["Location"] == "/tasks/"


def test_delete_task_post(client: Client) -> None:
    # given
    task = create_task()
    client.force_login(task.author)
    task_id = task.id
    route = f"/tasks/{task_id}/delete/"

    # when
    response = client.post(route)

    # then
    assert Task.objects.count() == 0
    assert response["Location"] == "/tasks/"
