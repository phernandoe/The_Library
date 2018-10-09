from datetime import datetime
from app import app, db
from flask import render_template, flash, redirect, url_for
from app.create_new_artist import createNewArtist
from app.models import Artist, Event, Venue, ArtistToEvent

artists = ["Kindo", "SnarkyPuppy", "Brasstracks", "Polyphia"]


@app.route('/')
@app.route('/index')
def index():
    intro = "A Library, but instead of a collection of books its a collection of music artists. Use the navigation " \
            "bar at the top to discover new artists along with information about them. Have fun! "

    return render_template('index.html', artists=artists, message=intro)


@app.route('/artist')
def artist():
    artistInfo = {"name": "Kindo",
                  "bio": "Kindo is an American rock band "
                         "originating from Buffalo, New York, currently "
                         "based out of New York City.They produce "
                         "and releasetheir music independently.",
                  "hometown": "Buffalo, New York",
                  "upcomingEvents": "No Upcoming Shows"}

    return render_template('artist.html', artistsInfo=artistInfo, artists=artists)


@app.route('/create_new_artist', methods=['GET', 'POST'])
def create_new_artist():
    form = createNewArtist()
    artistInfo = {
        "name": form.name.data,
        "hometown": form.hometown.data,
        "bio": form.description.data
    }

    if form.validate_on_submit():
        flash('{} has been added to the library'.format(form.name.data))
        return render_template('artist.html', artistsInfo=artistInfo)

    return render_template('create_new_artist.html', artists=artists, title='Create new artist', form=form)

@app.route('/reset_db')
def reset_db():

    flash("Resetting database: existing data will be replaced with default data")
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    # artists = [{"Kindo", "Rock"}, {"Brasstracks", "Jazz"}, {"Polyphia", "Rock"}]
    # venues = [{"The Haunt", "Ithaca, NY", 300}, {"Kilpatricks", "Ithaca, NY", 100}, {"Lost Horizon", "Syracuse, NY", 250}]
    # events = [{"Grand Slam", "01/01/2018", 1}, {"Dunk", "05/05/2018", 2}, {"Buzzer", "09/23/2018", 1}]
    # artistToEvents = [{1, 1}, {2, 1}, {3, 2}, {2, 2}, {3, 3}]

    a = Artist(name="Blah", genre="Punk")
    db.session.add(a)
    db.session.flush()

    v = Venue(name="The Haunt", location="Ithaca, NY", capacity=300)
    db.session.add(v)
    db.session.flush()

    e = Event(name="Dunk", time=datetime.utcnow(), venueID=v.id)
    db.session.add(e)
    db.session.flush()

    ae = ArtistToEvent(artistID=a.id, eventID=e.id)
    db.session.add(ae)
    db.session.flush()
    db.session.commit()

    ar = Artist.query.filter_by(name="Blah").first_or_404()

    return render_template('index.html', artists=artists, message=ar)
