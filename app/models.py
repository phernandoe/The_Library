from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Artist(db.Model):
    __tablename__ = "Artist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    genre = db.Column(db.String(64), index=True)
    hometown = db.Column(db.String(64))
    description = db.Column(db.String(128), index=True)
    events = db.relationship("ArtistToEvent", back_populates="artist")

    def __repr__(self):
        return '<ID: {}, Artist: {}, Genre: {}>'.format(self.id, self.name, self.genre)

class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    time = db.Column(db.DateTime, index=True)
    venueID = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artists = db.relationship("ArtistToEvent", back_populates="event")

    def __repr__(self):
        return '<ID: {}, Event: {}, Date: {}>'.format(self.id, self.name, self.time)

class Venue(db.Model):
    __tablename__ = "Venue"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    location = db.Column(db.String(64), index=True)
    capacity = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<ID: {}, Venue: {}, Location: {}>'.format(self.id, self.name, self.location)

class ArtistToEvent(db.Model):
    __tablename__ = "ArtistToEvent"
    id = db.Column(db.Integer, primary_key=True)
    artist = db.relationship("Artist", back_populates="events")
    event = db.relationship("Event", back_populates="artists")
    artistID = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    eventID = db.Column(db.Integer, db.ForeignKey('Event.id'), primary_key=True)

    def __repr__(self):
        return '<ID: {}, Artist: {}, Event: {}>'.format(self.id, self.artistID, self.eventID)
