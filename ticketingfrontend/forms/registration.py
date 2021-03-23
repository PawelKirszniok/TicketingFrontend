from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class UserRegistrationForm(FlaskForm):

    login = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(max=50), EqualTo('password')])
    name = StringField('Real Name',  validators=[DataRequired(), Length(max=100)])
    position = StringField('Position',  validators=[DataRequired(), Length(max=50)])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Sign Up')