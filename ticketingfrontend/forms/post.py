from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

status_options = [('Open', 'Open'), ('In Progress', 'In Progress'), ('Waiting for response', 'Waiting for response'),
                  ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Escalated', 'Escalated') ]


class NewPostForm(FlaskForm):
    new_status = SelectField('Change Status', choices=status_options)
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit Post')