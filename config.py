""" Flask Config """
from os import environ, path, getenv
from dotenv import load_dotenv
from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env('SECRET_KEY')

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """ Set Flask Config variable"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = SECRET_KEY
    API_KEY = getenv('API_KEY')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'PROD_DATABASE_URI'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres:///cinetrail'
