from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms_alchemy import ModelForm, model_form_factory
from wtforms.validators import Email
from wtforms import PasswordField, widgets
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(15), primary_key=True)
    first_name = db.Column(db.String(15), nullable=False,
                           info={'label': 'First Name'})
    last_name = db.Column(db.String(15), nullable=False,
                          info={'label': 'Last Name'})
    password = db.Column(db.String, nullable=False, info={
                         'form_field_class': PasswordField})
    email = db.Column(db.String, nullable=False, unique=False,
                      info={'validators': Email()})
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd, 14)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)
    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate

    def __repr__(self):
        u = self
        return f'<Username={u.username} name={u.first_name} {u.last_name}, email={u.email}>'


class Show(db.Model):

    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, info={
                     'widget': widgets.HiddenInput()})
    rating = db.Column(db.Float, info={'widget': widgets.HiddenInput()})
    summary = db.Column(db.String, info={'widget': widgets.HiddenInput()})
    url = db.Column(db.String, nullable=False, info={
                    'widget': widgets.HiddenInput()})
    img_url = db.Column(db.String, info={'widget': widgets.HiddenInput()})
    api_id = db.Column(db.Integer, nullable=False, unique=True,
                       info={'widget': widgets.HiddenInput()})
    episodes = db.relationship('Episode', backref='shows')
    seasons = db.relationship('Season', backref='shows')
    watch_status = db.relationship('Watched_show', backref='shows')

    def __repr__(self):
        s = self
        return f'<Show={s.name}>'


class Season(db.Model):

    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True)
    season_num = db.Column(db.Integer, nullable=False)
    api_id = db.Column(db.Integer, nullable=False, unique=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    episodes = db.relationship('Episode', backref='seasons')
    watched = db.relationship(
        'Watched_season', backref='episodes')


class Episode(db.Model):

    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey(
        'seasons.api_id'), nullable=False)
    summary = db.Column(db.String)
    number = db.Column(db.Integer)
    api_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    watched = db.relationship(
        'Watched_episode', backref='episodes')

    def __repr__(self):
        e = self
        return f'<Ep={e.name}, season={e.season_id}, shows={e.show_id}>'


class Watched_show(db.Model):

    __tablename__ = 'watched_shows'

    user_id = db.Column(db.String, db.ForeignKey(
        'users.username'), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey(
        'shows.id'), primary_key=True)
    liked = db.Column(db.Boolean, default=False)
    finished = db.Column(db.Boolean, default=False)
    watching = db.Column(db.Boolean, default=False)

class Watched_season(db.Model):

    __tablename__='watched_season'

    user_id = db.Column(db.String, db.ForeignKey(
        'users.username'), primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey(
        'seasons.id'), primary_key=True)
    finished = db.Column(db.Boolean, nullable=False, default=False)    

class Watched_episode(db.Model):

    __tablename__ = 'watched_episodes'

    user_id = db.Column(db.String, db.ForeignKey(
        'users.username'), primary_key=True)
    ep_id = db.Column(db.Integer, db.ForeignKey(
        'episodes.id'), primary_key=True)
    liked = db.Column(db.Boolean, default=False)
    finished = db.Column(db.Boolean, default=False)


class Show_queue(db.Model):

    ___tablename__ = "show_queue"

    user_id = db.Column(db.String, db.ForeignKey(
        'users.username'), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey(
        'shows.id'), primary_key=True)
    marked_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    interest_level = db.Column(db.Integer, nullable=False)


class Youtube_vid(db.Model):

    __tablename__ = 'youtube_vids'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    thumbnail = db.Column(db.String, nullable=False)
    liked = db.Column(db.Boolean)


class Search(db.Model):
    __tablename__ = 'searches'

    search_value = db.Column(db.String, primary_key=True)
    result = db.Column(db.ARRAY(db.String), nullable=False, default=['string'])


def connect_db(app):

    db.app = app
    db.init_app(app)
