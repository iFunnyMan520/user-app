from flask import render_template, request, Response, jsonify
from flask.views import MethodView
from marshmallow import ValidationError

from components.users import inputs, exc
from components.users.decorators import authorized, superuser
from components.users.models import User


class UserView(MethodView):
    @authorized
    def get(self, user: 'User'):
        users = User.get_all_users()
        return render_template('pages/users/index.html', users=users,
                               current_user=user)

    @superuser
    def post(self, user: 'User'):
        try:
            data = inputs.SignInSchema().load(request.json)
            new_user = User.create(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                superuser=data['superuser']
            )
            return jsonify(new_user.serialize())

        except ValidationError:
            return Response(status=400)
        except exc.EmailAlreadyExisted:
            return Response(status=403)

    @superuser
    def put(self, user: 'User'):
        try:
            data = inputs.EditUserSchema().load(request.json)
            edited_user = User.edit(
                user_id=data['user_id'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                superuser=data['superuser']
            )

            if not edited_user:
                return Response(status=404)

            return jsonify(edited_user.serialize())

        except ValidationError:
            return Response(status=400)
        except exc.EmailAlreadyExisted:
            return Response(status=403)

    @superuser
    def delete(self, user: 'User'):
        try:
            data = inputs.UserIdSchema().load(request.json)
            deleted_user = User.get_user(user_id=data['user_id'])

            if not deleted_user:
                return Response(status=404)

            deleted_user.delete()

            return Response(status=200)
        except ValidationError:
            return Response(status=400)
