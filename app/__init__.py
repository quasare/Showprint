import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from .models import db, connect_db
from .shows.show_routes import shows
from .users.users_routes import user
from .anime.anime_routes import anime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///cinetrail'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)    

connect_db(app)


with app.app_context():
    db.create_all()

app.register_blueprint(shows, url_prefix='/shows')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(anime, url_prefix='/anime')

@app.route('/')
def landing():
    return render_template('layout.html')    