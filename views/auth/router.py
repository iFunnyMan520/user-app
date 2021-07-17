from flask import Flask

from views.auth import handlers


def install(app: Flask):
    app.add_url_rule(
        '/login/',
        view_func=handlers.LoginView().as_view('login'),
        methods=['GET', 'POST']
    )
    app.add_url_rule(
        '/signIn/',
        view_func=handlers.SignInView().as_view('signIn'),
        methods=['GET', 'POST']
    )
    app.add_url_rule(
        '/logout/',
        view_func=handlers.LogoutView().as_view('logout')
    )
