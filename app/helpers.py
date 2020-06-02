from flask import session, request, redirect, url_for, flash
from functools import wraps
import requests
import os
from environs import Env

env = Env()
env.read_env()

API_KEY = env('API_KEY')

BASE_URL = 'https://www.googleapis.com/youtube/v3/search'


# Login Auth decorator
def login_required(f):
    @wraps(f)
    def decoratee_fucntion(*args, **kwargs):
        if 'username' not in session:
            flash('Please login to view this page', 'danger')
            return redirect(url_for('landing'))
        return f(*args, **kwargs)    
    return decoratee_fucntion    