import os
from unittest import TestCase

from ..models import db, connect_db


# Import db


from app import create_app

create_app('TestConfig')

