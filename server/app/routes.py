from app import app
from flask import render_template, Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Volumes/XTRADISK/friendly-forensics/server/uploaded'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
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
    return render_template('index.html', title='Home')

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
