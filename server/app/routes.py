from app import app
from flask import render_template, request, Markup, Flask, redirect, url_for, json
#import mysql.connector as mariadb
import pymysql
pymysql.install_as_MySQLdb()

upload_location = '.'


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    bodyText = "here"
    # bodyText = Markup("<b> my text </b>")
    # a = connect_to_db('user@localhost', 'password', 'varlog')
    # add_primary_key(a, "varlog", "filename")
    return render_template('basic.html', bodyText=bodyText)


@app.route('/insert/<msg>', methods=['POST', 'GET'])
def insert(msg):
    return render_template('basic.html', bodyText=msg)



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


def connect_to_db(username, pswd, db):
    cursor = None
    try:
        mariadb_connection = pymysql.connect(user=username, password=pswd, database=db)
        cursor = mariadb_connection.cursor()
    except:
        print("Failed to connect to db.")
    return cursor


def add_primary_key(cursor, tablename, primaryKeyValue):
    try:
        cursor.execute("alter table %s add primary key(%s)" % (tablename, primaryKeyValue))
    except:
        print("Failed to insert into db.")
