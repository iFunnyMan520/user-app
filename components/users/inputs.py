from marshmallow import Schema, fields


class LoginSchema(Schema):
    email: str = fields.String(required=True)
    password: str = fields.String(required=True)


class SignInSchema(LoginSchema):
    first_name: str = fields.String(required=True)
    last_name: str = fields.String(required=True)
    superuser: bool = fields.Boolean(required=True)


class UserIdSchema(Schema):
    user_id: int = fields.Integer(required=True)


class EditUserSchema(UserIdSchema):
    email: str = fields.String(required=True)
    first_name: str = fields.String(required=True)
    last_name: str = fields.String(required=True)
    superuser: bool = fields.Boolean(required=True)
