from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'file': 'file1',
            'body': 'test data for file 1'
        },
        {
	    'file': 'file2',
            'body': 'test data for file 2'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
