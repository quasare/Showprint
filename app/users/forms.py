from flask_wtf import FlaskForm
from ..models import db, User
from wtforms_alchemy import model_form_factory
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class RegisterUserForm(ModelForm):
    class Meta:
        include = ['username']
        model = User


class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])


class EditUserForm(ModelForm):
    class Meta:
        model = User
