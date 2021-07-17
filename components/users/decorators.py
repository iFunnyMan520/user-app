from flask import request, redirect, Response

from components.users.models import User


def authorized(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token', None)

        if not token:
            return redirect('/login/')

        user = User.get_user(token=token)

        if not user:
            return redirect('/login/')

        kwargs['user'] = user
        response = func(*args, **kwargs)

        return response
    return wrapper


def superuser(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token', None)

        if not token:
            return redirect('/login/')

        user = User.get_user(token=token)

        if not user:
            return redirect('/login/')

        if not user.superuser:
            return Response(status=403)

        kwargs['user'] = user
        response = func(*args, **kwargs)

        return response
    return wrapper
