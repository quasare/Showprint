from flask_wtf import FlaskForm
from ..models import Language, Stack, Technology, Extensions, Framework, Tutorial, db
from wtforms_alchemy import  model_form_factory
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session