from flask import Flask, Response
from flask.testing import FlaskClient


class AuthClient:

    def __init__(self, app: Flask):
        self.client: FlaskClient = app.test_client(use_cookies=True)

    def register(self,
                 email: str,
                 password: str,
                 first_name: str,
                 last_name: str,
                 superuser: bool = False) -> Response:
        return self.client.post('/signIn/', json={
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'superuser': superuser,
        })

    def login(self, email: str, password: str) -> Response:
        return self.client.post('/login/', json={
            'email': email,
            'password': password,
        })

    def logout(self) -> Response:
        return self.client.get('/logout/')
