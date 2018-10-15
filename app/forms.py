from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Artist, User, Venue

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

class createNewVenue(FlaskForm):
    name = StringField('Name', validators=[DataRequired("No name provided")])
    location = StringField('Location', validators=[DataRequired("No location provided")])
    capacity = IntegerField('Capacity')

    submit = SubmitField('Add Venue')

    def validate_name(self, name):
        venue = Venue.query.filter_by(name=name.data).first()
        if venue is not None:
            raise ValidationError("Venue already exists")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already exists.')
