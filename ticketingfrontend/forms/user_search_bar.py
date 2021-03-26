from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class UserSearchBar(FlaskForm):
    search_string = StringField('Search for developer', validators=[DataRequired()])
    search = SubmitField('Add developer')