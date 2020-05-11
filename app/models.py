from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms_alchemy import ModelForm, model_form_factory


db = SQLAlchemy()


class User(db.Model):

    __tablename__='users'

    username = db.Column(db.String(15), primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        u = self
        return f'<Username={u.username} name={u.first_name} {u.last_name}, email={u.email}>'


class Show(db.Model):

    __tablename__='shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    summary = db.Column(db.String, nullable=False)
    episodes = db.relationship('episodes', backref='shows')
    seasons = db.relationship('season', backref='shows')

    def __repr__(sefl):
        s = self
        return f'<Show={s.name}>'

class Season(db.Model):

    __tablename__='seasons'

    id = db.Column(db.Integer, primary_key=True)
    season_num = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    episodes = db.relationship('episodes', backref='seasons')

class Episode(db.Model):

    __tablename__='episodes' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False) 
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False )
    summary = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)

    def __repr__(sefl):
        e = self
        return f'<Ep={e.name}, season={e.season}, shows={e.show_id}>'     

class Watched_show(db.Model):

    __tablename__='watched_shows'

    user_id = db.Column(db.String, db.ForeignKey('users.username'), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), primary_key=True)
    liked = db.Column(db.Boolean, default=False)

class Watched_episode(db.Model):
    
    __tablename__='watched_episodes'

    user_id = db.Column(db.String, db.ForeignKey('users.username'), primary_key=True)
    ep_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), primary_key=True)
    liked = db.Column(db.Boolean, default=False)

class Show_queue(db.Model):

    ___tablename__="show_queue"

    user_id = db.Column(db.String, db.ForeignKey('users.username'), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), primary_key=True)
    marked_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    interest_level = db.Column(db.Integer, nullable=False)

class Youtube_vid(db.Model):

    __tablename__='youtube_vids'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    thumbnail = db.Column(db.String, nullable=False)
    liked = db.Column(db.Boolean)

def connect_db(app):
    
    db.app = app
    db.init_app(app)