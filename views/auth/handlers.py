from flask import render_template, request, Response, redirect
from flask.views import MethodView
from marshmallow import ValidationError

from components.users import inputs, exc
from components.users.decorators import authorized
from components.users.models import User


class LoginView(MethodView):
    def get(self):
        if request.cookies.get('token', None):
            return redirect('/')
        return render_template('pages/login/index.html')

    def post(self):
        try:
            data = inputs.LoginSchema().load(request.json)
            user = User.login(data['email'], data['password'])

            response = Response(status=200)
            response.set_cookie('token', user.token)

            return response

        except ValidationError:
            return Response(status=400)
        except exc.AuthUserNotFound:
            return Response(status=404)


class SignInView(MethodView):
    def get(self):
        if request.cookies.get('token', None):
            return redirect('/')
        return render_template('pages/signIn/index.html')

    def post(self):
        try:
            data = inputs.SignInSchema().load(request.json)
            user = User.register(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                superuser=data['superuser']
            )

            response = Response(status=200)
            response.set_cookie('token', user.token)

            return response

        except ValidationError:
            return Response(status=400)
        except exc.EmailAlreadyExisted:
            return Response(status=403)


class LogoutView(MethodView):
    @authorized
    def get(self, user: 'User'):
        user.logout()
        response = Response(status=200)
        response.delete_cookie('token')

        return response
