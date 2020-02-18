from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jake'}
    posts = [
        {
            'author' : {'username' : 'John'},
            'body' : 'Quadsort is pretty neat!'
        },
        {
            'author' : {'username' : 'Jane'},
            'body' : 'Is quicksort a thing of the past?'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)