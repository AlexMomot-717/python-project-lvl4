import pytest
from django.template.response import TemplateResponse
from django.test import Client
from freezegun import freeze_time
from task_manager.users.forms import ServiceUserForm
from task_manager.users.models import ServiceUser

pytestmark = pytest.mark.django_db


@freeze_time("15.07.2024 17:00")
def test_users_list(client: Client) -> None:
    # given
    ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="x", password="%%%%%"
    )
    route = "/users/"
    users = ServiceUser.objects.all()

    # when
    response = client.get(route)

    # then
    context = {"users": users}
    expected_html = TemplateResponse(
        response.wsgi_request, "users_list.html", context=context
    ).render()
    assert response.content.decode() == expected_html.content.decode()
    assert response.status_code == 200


@freeze_time("15.07.2024 17:00")
def test_create_user_get(client: Client) -> None:
    # given
    route = "/users/create/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    form = ServiceUserForm()
    context = {"form": form, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "create_user.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


@freeze_time("15.07.2024 17:00")
def test_create_user_post(client: Client) -> None:
    # given
    route = "/users/create/"
    form_data = {
        "first_name": "taylor",
        "last_name": "swift",
        "username": "alison",
        "password1": "*****",
        "password2": "*****",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert ServiceUser.objects.get(id=1).username == "alison"
    assert response["Location"] == "/login/"


@freeze_time("15.07.2024 17:00")
def test_edit_user_get_user_is_logged_in(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    client.force_login(service_user)
    user_id = service_user.id
    route = f"/users/{user_id}/edit/"

    # when
    client.force_login(service_user)
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    form = ServiceUserForm(instance=service_user)
    context = {"form": form, "user_id": user_id, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "update_user.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


@freeze_time("15.07.2024 17:00")
def test_edit_user_get_user_is_not_logged_in(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    user_id = service_user.id
    route = f"/users/{user_id}/edit/"

    # when
    response = client.get(route)

    # then
    assert "login" in response["Location"]


@freeze_time("15.07.2024 17:00")
def test_edit_user_get_requestuser_is_not_objectuser(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    client.force_login(service_user)
    object_user_id = ServiceUser.objects.create(
        first_name="taylor", last_name="swift", username="alison", password="*****"
    ).id
    route = f"/users/{object_user_id}/edit/"

    # when
    response = client.get(route)

    # then
    assert response["Location"] == "/users/"


@freeze_time("15.07.2024 17:00")
def test_edit_user_objectuser_does_not_exist(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    client.force_login(service_user)
    object_user_id = 2
    route = f"/users/{object_user_id}/edit/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


@freeze_time("15.07.2024 17:00")
def test_edit_user_post(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    client.force_login(service_user)
    user_id = service_user.id
    route = f"/users/{user_id}/edit/"
    form_data = {
        "first_name": "taylor",
        "last_name": "swift",
        "username": "alison",
        "password1": "*****",
        "password2": "*****",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert (
        ServiceUser.objects.get(id=user_id).username == "alison"
    )  # password is hashed with sha256
    assert response["Location"] == "/users/"


@freeze_time("15.07.2024 17:00")
def test_edit_user_post_form_is_not_valid(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    client.force_login(service_user)
    user_id = service_user.id
    route = f"/users/{user_id}/edit/"
    form_data = {
        "first_name": "",
        "last_name": "",
        "username": "alison",
        "password1": "",
        "password2": "",
    }

    # when
    response = client.post(route, data=form_data)

    # then
    assert ServiceUser.objects.get(id=1) == service_user
    assert response.status_code == 200


@freeze_time("15.07.2024 17:00")
def test_delete_user_get_user_is_logged_in(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    client.force_login(service_user)
    user_id = service_user.id
    route = f"/users/{user_id}/delete/"

    # when
    response = client.get(route)
    csrf_token = response.context.get("csrf_token")
    context = {"user": service_user, "csrf_token": csrf_token}

    # then
    expected_html = TemplateResponse(
        response.wsgi_request, "delete_user.html", context=context
    ).render()
    assert expected_html.content == response.content
    assert response.status_code == 200


@freeze_time("15.07.2024 17:00")
def test_delete_user_get_user_is_not_logged_in(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    user_id = service_user.id
    route = f"/users/{user_id}/delete/"

    # when
    response = client.get(route)

    # then
    assert "login" in response["Location"]


@freeze_time("15.07.2024 17:00")
def test_delete_user_objectuser_does_not_exist(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    client.force_login(service_user)
    object_user_id = 2
    route = f"/users/{object_user_id}/delete/"

    # when
    response = client.get(route)

    # then
    assert response.status_code == 404


@freeze_time("15.07.2024 17:00")
def test_delete_user_post(client: Client) -> None:
    # given
    service_user = ServiceUser.objects.create(
        first_name="ilon", last_name="mask", username="ilon-mask", password="%%%%%"
    )
    user_id = service_user.id
    route = f"/users/{user_id}/delete/"

    # when
    client.force_login(service_user)
    response = client.post(route)

    # then
    assert ServiceUser.objects.count() == 0
    assert response["Location"] == "/users/"
