from flask import Flask

from views.users import handlers


def install(app: Flask):
    app.add_url_rule(
        '/',
        view_func=handlers.UserView().as_view('users'),
        methods=['GET', 'POST', 'PUT', 'DELETE']
    )
