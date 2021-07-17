class EmailAlreadyExisted(Exception):
    """ Raise when user with submitted email already existed """


class AuthUserNotFound(Exception):
    """ Raise when user with submitted data doesn't exist """
