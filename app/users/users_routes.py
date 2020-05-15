from flask import Blueprint, render_template, session
from flask_security import Security, SQLAlchemyUserDatastore, login_required
from .forms import RegisterUserForm
from ..models import db, User




user = Blueprint('user', __name__, template_folder='templates',
                     static_folder='static')


@user.route('/')
def user_dashboard():
    return render_template('user_dashboard.html')

  