from app import app
from flask import render_template

artists = ["Kindo", "SnarkyPuppy", "Brasstracks", "Polyphia"]

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html', artists=artists)

@app.route('/Kindo')
def kindo():

    name = "Kindo"
    bio = "Kindo is an American rock band " \
          "originating from Buffalo, New York, currently " \
          "based out of New York City.They produce " \
          "and releasetheir music independently."
    hometown = "Buffalo, New York"
    upcomingEvents = "No Upcoming Shows"

    return render_template('kindo.html', artists=artists, name=name, bio=bio, hometown=hometown, upcomingEvents=upcomingEvents)

@app.route('/create_new_artist')
def create_new_artist():
    return render_template('create_new_artist.html', artists=artists)