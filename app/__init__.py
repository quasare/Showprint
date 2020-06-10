import os
from flask import Flask, render_template, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from .models import db, connect_db
from .shows.show_routes import shows
from .users.users_routes import user
from .auth.auth_routes import auth
from .users.forms import RegisterUserForm, LoginForm
from datetime import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object('config.DevConfig')
toolbar = DebugToolbarExtension(app)

connect_db(app)


with app.app_context():
    db.create_all()

app.register_blueprint(shows, url_prefix='/shows')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(auth)


@app.route('/')
def landing():
    if 'username' in session:
        return redirect(url_for(user.user_dashboard))
    return render_template('landing.html')
