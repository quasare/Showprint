import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from .models import db, connect_db, User
from .shows.show_routes import shows
from .users.users_routes import user
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


@app.route('/')
def landing():
    return render_template('layout.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        try:

            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            registerd = User.register(username, password)
            user = User(username=username, password=registerd.password,
                        email=email, first_name=first_name, last_name=last_name)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)

        session["username"] = user.username
        return redirect(url_for('user.user_dashboard'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            user.last_login = datetime.now()
            db.session.commit()
            session["username"] = user.username  # keep logged in
            return redirect(url_for('user.user_dashboard'))
        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('landing'))
