import functools
from flask import session, redirect

def authentication(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        if 'email' not in session:
            return redirect('/mainhome')
        return view_func(*args, **kwargs)
    return decorated


def guest(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        if 'email' in session:
            return redirect('/home')
        return view_func(*args, **kwargs)
    return decorated