from flask import redirect, session


def is_authenticated():
    return 'username' in session


def requires_authentication(func):
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect('/')
        return func(*args, **kwargs)

    return wrapper


def requires_admin_role(func):
    def wrapper(*args, **kwargs):
        if 'username' not in session or session['username'] != 'admin':
            return 'You don\'t have permission to acces this URL'
        return func(*args, **kwargs)
    return wrapper
