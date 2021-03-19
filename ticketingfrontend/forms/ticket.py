from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
import re

class NewTicketForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=100)])
    status = StringField('status', validators=[DataRequired(), Length(max=30)])
    deadline = StringField('dd-mm-yy', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField("Create Ticket")

    def validate_deadline(self, form):
        if not re.search(r'\d{2}-\d{2}-\d{2}', form.data):
            raise ValidationError('Invalid Date, use the  DD-MM-YY format')

