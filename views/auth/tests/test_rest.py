import pytest

from views.auth.tests.rest_client import AuthClient


@pytest.fixture
def client(server_app):
    auth_client = AuthClient(server_app)
    return auth_client


def test_register(client: AuthClient):
    response = client.register(
        email='first_email@gmail.com',
        password='qwerty',
        first_name='First',
        last_name='Last'
    )
    assert response.status_code == 200

    response = client.register(
        email='first_email@gmail.com',
        password='qwerty',
        first_name='First',
        last_name='Last'
    )
    assert response.status_code == 403


def test_login(client: AuthClient):
    response = client.login('first_email@gmail.com', 'qwert')
    assert response.status_code == 404

    response = client.login('second_email@gmail.com', 'qwerty')
    assert response.status_code == 404

    response = client.login('first_email@gmail.com', 'qwerty')
    assert response.status_code == 200
