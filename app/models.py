from app import db

class Artist(db.Model):
    __tablename__ = "Artist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    genre = db.Column(db.String(64), index=True)
    events = db.relationship("ArtistToEvent", back_populates="artist")

    def __repr__(self):
        return '<Artist {}, Genre {}>'.format(self.name, self.genre)

class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    time = db.Column(db.DateTime, index=True)
    venueID = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artists = db.relationship("ArtistToEvent", back_populates="event")

    def __repr__(self):
        return '<Event {}, Date {}>'.format(self.name, self.datetime)

class Venue(db.Model):
    __tablename__ = "Venue"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    location = db.Column(db.String(64), index=True)
    capacity = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Venue {}, Location {}>'.format(self.name, self.location)

class ArtistToEvent(db.Model):
    __tablename__ = "ArtistToEvent"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist = db.relationship("Artist", back_populates="events")
    event = db.relationship("Event", back_populates="artists")
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Event.id'), primary_key=True)

    def __repr__(self):
        return 'Artist {}, Event {}>'.format(self.artist_id, self.event_id)
