from flask import Flask


def make_app() -> Flask:
    from views.auth.router import install as auth_router
    from views.users.router import install as users_router

    app = Flask(__name__)

    auth_router(app)
    users_router(app)

    return app
