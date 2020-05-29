from flask import session, request, redirect, url_for, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decoratee_fucntion(*args, **kwargs):
        if 'username' not in session:
            flash('Please login to view this page', 'danger')
            return redirect(url_for('landing'))
        return f(*args, **kwargs)    
    return decoratee_fucntion    