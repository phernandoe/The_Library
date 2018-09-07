from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():

    user = {'username': 'Fernando'}

    posts = [
        {
            'author': {'username': 'Fernando'},
            'body': 'Beautiful day in Ithaca!'
        },
        {
            'author': {'username': 'Lee'},
            'body': 'What should I have for dinner?'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/hidden')
def hidden():

    return render_template('index.html', title='Oh No', secret="Hello World!")




