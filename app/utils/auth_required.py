from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Access denied! Please log in.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None or session.get('role') != 'admin':
            flash("Access denied! Admins only.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function