from flask_wtf import FlaskForm
from ..models import Show, db
from wtforms_alchemy import  model_form_factory
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Email, Length


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

# class LanguageForm(ModelForm):
#     class Meta:
#         include = ['name']
#         model = Show

class SearchForm(FlaskForm):
    """Search Form for API call"""

    search = StringField(" ", validators=[InputRequired(), Length(max=30)])


class AddShowForm(ModelForm):
    class Meta: 
        model = Show



