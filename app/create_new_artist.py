from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from app.models import Artist


class createNewArtist(FlaskForm):
    name = StringField('Name', validators=[DataRequired("No name provided")])
    genre = StringField('Genre')
    hometown = StringField('Hometown')
    description = TextAreaField('Description')

    submit = SubmitField('Add Artist')

    def validate_name(self, name):
        artist = Artist.query.filter_by(name=name.data).first()
        if artist is not None:
            raise ValidationError("Artist has already been registered")
