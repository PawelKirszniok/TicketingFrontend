from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class UserLoginForm(FlaskForm):

    login = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password',  validators=[DataRequired(), Length(max=50)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

