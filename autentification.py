from flask import redirect, session
from functools import wraps


def is_authenticated():
    return session['username'] is not '' or session['admin_flag'] is True


def requires_authentication(func):
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect('/')
        return func(*args, **kwargs)

    return wrapper


def requires_admin_role(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session['username'] is not '' and session['admin_flag'] is False:
            return 'You don\'t have permission to access this URL'
        return func(*args, **kwargs)
    return wrapper


def requires_authentication2(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect('/')
        return func(*args, **kwargs)

    return decorated_function
