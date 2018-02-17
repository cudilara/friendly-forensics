from app import app
from flask import render_template, request

@app.route('/')
@app.route('/index', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST' or request.method == 'GET':
        data = request.args.get('name')
        # if data == None:
        #     data = "Did not receive data."
    return render_template('index.html', title='Home', post=data)

def import_data():
    r = None
    try:
        if request.files:
            r = request.files
    except:
        print("Failed to receive file.")
    return r

# @app.route('/upload/', methods=['GET', 'POST'])
# def upload():
#    if request.method == 'POST':
#       file = request.files['file']
#       if file:
#         file.read()
#         a = 'file uploaded'
#    return render_template("index.html", post = a)