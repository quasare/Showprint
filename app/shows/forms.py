from flask_wtf import FlaskForm
from ..models import Show
from wtforms_alchemy import  model_form_factory
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class LanguageForm(ModelForm):
    class Meta:
        include = ['name']
        model = Show



