#!/usr/bin/env python
from flask import render_template, request, Markup, Flask, redirect, url_for, json
# import pymysql
# pymysql.install_as_MySQLdb()

upload_location = '.'
myhost = '0.0.0.0'
myport = 4000
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('basic.html')

@app.route('/', methods=['POST'])
def index():
    bodyText = "Welcome to Madinger's thesis project!"
    if request.form['investigation_name'] != "":
        investigationName = request.form['investigation_name']
        investigationName = "Data for: " + investigationName
        return render_template('basic.html', bodyText=bodyText, acceptedName=investigationName)
    else:
        return render_template('basic.html', bodyText=bodyText)

if __name__ == '__main__':
    app.debug = True
    app.run(host = myhost, port = myport)
