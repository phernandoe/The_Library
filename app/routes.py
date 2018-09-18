from app import app
from flask import render_template, flash, redirect, url_for
from app.create_new_artist import createNewArtist

artists = ["Kindo", "SnarkyPuppy", "Brasstracks", "Polyphia"]


@app.route('/')
@app.route('/index')
def index():
    intro = "A Library, but instead of a collection of books its a collection of music artists. Use the navigation " \
            "bar at the top to discover new artists along with information about them. Have fun! "

    return render_template('index.html', artists=artists, intro=intro)


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
