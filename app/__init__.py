import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from .models import db, connect_db
from .shows.show_routes import shows

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

@app.route('/')
def landing():
    return render_template('layout.html')    