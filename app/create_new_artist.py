from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class createNewArtist(FlaskForm):
    name = StringField('Name', validators=[DataRequired("No name provided")])
    hometown = StringField('Hometown')
    description = TextAreaField('Description')

    submit = SubmitField('Add Artist')
