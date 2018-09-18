from app import app
from flask import render_template, flash, redirect, url_for
from app.create_new_artist import createNewArtist

artists = ["Kindo", "SnarkyPuppy", "Brasstracks", "Polyphia"]


@app.route('/')
@app.route('/index')
def index():
    intro = "A Library, but instead of a collection of books its a collection of music artists. Use the navigation bar at the top to discover newartists along with information about them. Have fun!"

    return render_template('index.html', artists=artists, intro=intro)


@app.route('/artist')
def artist():
    artistInfo = {
        "Kindo":
            {"name": "Kindo",
             "bio": "Kindo is an American rock band "
                    "originating from Buffalo, New York, currently "
                    "based out of New York City.They produce "
                    "and releasetheir music independently.",
             "hometown": "Buffalo, New York",
             "upcomingEvents": "No Upcoming Shows"},

        "Snarky Puppy":
            {"name": "Snarky Puppy",
             "bio": "Snarky Puppy is a Brooklyn-based ...fusion-influenced "
                    "jam band... led by bassist, composer, and producer Michael "
                    "League. Snarky Puppy combines jazz, rock, and funk and has"
                    " won three Grammy Awards.",
             "hometown": "Denton, Texas",
             "upcomingEvents": "No Upcoming Shows"},

        "Brasstracks":
            {"name": "Brasstracks",
             "bio": "Horns, Synth, Drums",
             "hometown": "New York, New York",
             "upcomingEvents": "No Upcoming Shows"},

        "Polyphia":
            {"name": "Polyphia",
             "bio": "Polyphia is an American instrumental progressive metal "
                    "band based in Dallas, Texas, formed in 2010.",
             "hometown": "Dallas, Texas",
             "upcomingEvents": "No Upcoming Shows"}
    }

    return render_template('artist.html', artistsInfo=artistInfo, artists=artists)


@app.route('/create_new_artist', methods=['GET', 'POST'])
def create_new_artist():

    form = createNewArtist()

    if form.validate_on_submit():
        flash('{} has been added to the library'.format(form.name.data))
        return redirect(url_for('artist'))

    return render_template('create_new_artist.html', artists=artists, title='Create new artist', form=form)
