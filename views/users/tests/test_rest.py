import pytest

from components.users.models import User
from views.users.tests.rest_client import UserClient


@pytest.fixture
def user_client(server_app):
    user_client = UserClient(server_app)
    return user_client


@pytest.fixture
def authorized_client(server_app, test_user):
    user_client = UserClient(server_app)
    user_client.login(test_user.email, 'qwerty')
    return user_client


@pytest.fixture
def authorized_super_client(server_app, test_superuser):
    user_client = UserClient(server_app)
    user_client.login(test_superuser.email, 'qwerty')
    return user_client


def test_user_list(user_client: UserClient,
                   authorized_super_client: UserClient):
    response = user_client.get_users()
    assert response.status_code == 302

    response = authorized_super_client.get_users()
    assert response.status_code == 200


def test_crud(authorized_client: UserClient,
              authorized_super_client: UserClient,
              test_user: User):
    response = authorized_client.create_user(
        email='asd@gmail.com',
        password='1234',
        first_name='A',
        last_name='B'
    )
    assert response.status_code == 403

    response = authorized_super_client.create_user(
        email='asd@gmail.com',
        password='1234',
        first_name='A',
        last_name='B'
    )
    assert response.status_code == 200
    assert response.get_json()['email'] == 'asd@gmail.com'
    user_id = response.get_json()['id']

    response = authorized_super_client.create_user(
        email='asd@gmail.com',
        password='1234',
        first_name='A',
        last_name='B'
    )
    assert response.status_code == 403

    response = authorized_super_client.edit_user(
        user_id=user_id,
        email='asdq@gmail.com',
        first_name='A',
        last_name='B'
    )
    assert response.status_code == 200
    assert response.get_json()['email'] == 'asdq@gmail.com'

    response = authorized_super_client.edit_user(
        user_id=user_id,
        email='test-user@gmail.com',
        first_name='A',
        last_name='B'
    )
    assert response.status_code == 403

    response = authorized_super_client.delete_user(user_id=user_id)
    assert response.status_code == 200

    assert User.get_user(user_id=user_id) is None


def test_logout(authorized_super_client: UserClient):
    response = authorized_super_client.logout()
    assert response.status_code == 200

    response = authorized_super_client.get_users()
    assert response.status_code == 302
