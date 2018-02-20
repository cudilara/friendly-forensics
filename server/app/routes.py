from app import app
from flask import render_template, request, Markup

upload_location = '.'


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    bodyText = import_data()
    # bodyText = Markup("<b> my text </b>")
    return render_template('basic.html', bodyText=bodyText)


def import_data():
    r = None
    try:
        # request.files returns ImmutableMultiDict([])
        if request.files:
            r = request.files
        else:
            r = "Did not get any files from clients."
            r = str(request.files)
    except:
        r = "Failed to receive file."
    return r
