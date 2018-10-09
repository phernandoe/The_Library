from datetime import datetime
from app import app, db
from flask import render_template, flash, redirect, url_for
from app.create_new_artist import createNewArtist
from app.models import Artist, Event, Venue, ArtistToEvent

artists = Artist.query

@app.route('/')
@app.route('/index')
def index():
    intro = "A Library, but instead of a collection of books its a collection of music artists. Use the navigation " \
            "bar at the top to discover new artists along with information about them. Have fun! "

    return render_template('index.html', artists=artists, message=intro)


@app.route('/artist/<name>')
def artist(name):
    artist = Artist.query.filter_by(name=name).first_or_404()
    venues = Venue.query
    events = Event.query
    a2e = ArtistToEvent.query.filter_by(artistID=artist.id).all()

    return render_template('artist.html', artist=artist, venue_list=venues, event_list=events, artistEvents=a2e)


@app.route('/create_new_artist', methods=['GET', 'POST'])
def create_new_artist():
    form = createNewArtist()

    if form.validate_on_submit():
        newArtist = Artist(name=form.name.data, genre=form.genre.data, hometown=form.hometown.data, description=form.description.data)
        db.session.add(newArtist)
        db.session.commit()
        flash('{} has been added to the library'.format(form.name.data))
        return render_template('artist.html', artist=newArtist)

    return render_template('create_new_artist.html', artists=artists, title='Create new artist', form=form)

@app.route('/reset_db')
def reset_db():

    flash("Resetting database: existing data will be replaced with default data")
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    kindo = Artist(name="Kindo", genre="Rock", hometown="Buffalo, NY", description="Very cool indie band")
    db.session.add(kindo)

    brasstracks = Artist(name="Brasstracks", genre="Jazz", hometown="New York, NY", description="Cool brass group")
    db.session.add(brasstracks)

    polyphia = Artist(name="Polyphia", genre="Rock", hometown="Dallas, TX", description="Best metal band ever")
    db.session.add(polyphia)
    db.session.flush()

    theHaunt = Venue(name="The Haunt", location="Ithaca, NY", capacity=200)
    db.session.add(theHaunt)

    kilpatricks = Venue(name="Kilpatricks", location="Ithaca, NY", capacity=100)
    db.session.add(kilpatricks)

    lostHorizon = Venue(name="Lost Horizon", location="Syracuse, NY", capacity=300)
    db.session.add(lostHorizon)
    db.session.flush()

    dunk = Event(name="Dunk", time=datetime.utcnow(), venueID=lostHorizon.id)
    db.session.add(dunk)

    grandSlam = Event(name="Grand Slam", time=datetime.utcnow(), venueID=lostHorizon.id)
    db.session.add(grandSlam)

    buzzer = Event(name="Buzzer", time=datetime.utcnow(), venueID=theHaunt.id)
    db.session.add(buzzer)
    db.session.flush()

    k2d = ArtistToEvent(artistID=kindo.id, eventID=dunk.id)
    db.session.add(k2d)

    b2d = ArtistToEvent(artistID=brasstracks.id, eventID=dunk.id)
    db.session.add(b2d)

    p2g = ArtistToEvent(artistID=polyphia.id, eventID=grandSlam.id)
    db.session.add(p2g)

    b2g = ArtistToEvent(artistID=brasstracks.id, eventID=grandSlam.id)
    db.session.add(b2g)

    p2b = ArtistToEvent(artistID=polyphia.id, eventID=buzzer.id)
    db.session.add(p2b)
    db.session.flush()
    db.session.commit()

    return render_template('index.html', artists=artists)
