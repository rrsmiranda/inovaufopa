
from flask import session, flash, redirect, url_for
from models import User
from functools import wraps
# from database import proxy

def auth_user(user):
    session['autenticad'] = True
    session['user_id'] = user.id
    session['username'] = user.username
    session['permissao'] = user.permissao
    flash('You are logged in as %s' % (user.username))


def acesso(permissao):
    user = get_current_user()
    if permissao in user.permissao.split(','):
        return True
    return False
    
def get_current_user():
    if session.get('autenticad'):
        return User.get(User.id == session['user_id'])

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('autenticad'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner

def acesso_required(permissao):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = get_current_user()
            if permissao not in user.permissao.split(','):
                return redirect(url_for('error'))
            return f(*args, **kwargs)
        return wrapped
    return decorator