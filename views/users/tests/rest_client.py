from flask import Response

from views.auth.tests.rest_client import AuthClient


class UserClient(AuthClient):

    def get_users(self) -> Response:
        return self.client.get('/')

    def create_user(self,
                    email: str,
                    password: str,
                    first_name: str,
                    last_name: str,
                    superuser: bool = False) -> Response:
        return self.client.post('/', json={
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'superuser': superuser,
        })

    def edit_user(self,
                  user_id: int,
                  email: str,
                  first_name: str,
                  last_name: str,
                  superuser: bool = False) -> Response:
        return self.client.put('/', json={
            'user_id': user_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'superuser': superuser,
        })

    def delete_user(self, user_id: int) -> Response:
        return self.client.delete('/', json={'user_id': user_id})
