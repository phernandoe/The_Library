from datetime import datetime

from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.urls import url_parse
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import createNewArtist, RegistrationForm, LoginForm, createNewVenue
from app.models import Artist, Event, Venue, ArtistToEvent, User

artists = Artist.query

@app.route('/')
@app.route('/index')
@login_required
def index():
    intro = "A Library, but instead of a collection of books its a collection of music artists. Use the navigation " \
            "bar at the top to discover new artists along with information about them. Have fun! "

    return render_template('index.html', artists=artists, message=intro)


@app.route('/lost')
def lost():
    message = "Hmm.. that artist does not currently exist in our records. Try creating a new artist page for them with the link above"

    return render_template('index.html', artists=artists, message=message)

@app.route('/artist/<name>')
def artist(name):
    artist = Artist.query.filter_by(name=name).first()

    if artist is None:
        return redirect(url_for('lost'))

    else:
        venues = Venue.query
        events = Event.query
        a2e = ArtistToEvent.query.filter_by(artistID=artist.id).all()

        return render_template('artist.html', artist=artist, venue_list=venues, event_list=events, artistEvents=a2e)


@app.route('/create_new_artist', methods=['GET', 'POST'])
@login_required
def create_new_artist():
    form = createNewArtist()

    if form.validate_on_submit():
        newArtist = Artist(name=form.name.data, genre=form.genre.data, hometown=form.hometown.data, description=form.description.data)
        db.session.add(newArtist)
        db.session.commit()
        flash('{} has been added to the library'.format(form.name.data))
        return render_template('artist.html', artist=newArtist)

    return render_template('create_new_artist.html', artists=artists, title='Create new artist', form=form)

@app.route('/create_new_venue', methods=['GET', 'POST'])
@login_required
def create_new_venue():
    form = createNewVenue()

    if form.validate_on_submit():
        newVenue = Venue(name=form.name.data, location=form.location.data, capacity=form.capacity.data)
        db.session.add(newVenue)
        db.session.commit()
        flash('{} has been added to the library'.format(form.name.data))
        return redirect(url_for('index'))

    return render_template('create_new_venue.html', artists=artists, title='Create new venue', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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

    user = User(username="Fernando", email="fernando@something.com")
    user.set_password("123")
    db.session.add(user)

    db.session.commit()

    return render_template('index.html', artists=artists)
