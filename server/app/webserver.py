#!/usr/bin/env python
from flask import render_template, request, Flask
import pymysql
import datetime

upload_location = '.'
myhost = '0.0.0.0'
myport = 4000
Root, Passwd, DBname = 'root', 'password', 'forensic_data'
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('basic.html')

@app.route('/', methods=['POST'])
def index():
    bodyText = "Welcome to Madinger's thesis project!"
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        print("Failed to connect to the database.")
        return render_template('basic.html')
    if request.form['investigation_name'] != "":
        investigationName = request.form['investigation_name']
        now = datetime.datetime.now()
        ins = "INSERT INTO Investigations(name_investigation,date_investigation) VALUES(%s, %s)"
        values = investigationName, now
        try:
            db_cursor.execute(ins, values)
            db_connection.commit()
        except:
            #TODO find investigation with that name
            print("Need to pull data for name ", investigationName)
        db_connection.close()
        investigationTitle = "Data for investigation: " + investigationName
        return render_template('basic.html', bodyText=bodyText, acceptedName=investigationTitle)
    else:
        return render_template('basic.html', bodyText=bodyText)

def connect_to_db(username, pswd, db):
    cursor = None
    mariadb_connection = None
    try:
        mariadb_connection = pymysql.connect(user=username, password=pswd, database=db)
        cursor = mariadb_connection.cursor()
    except:
        print("Failed to connect to db.")
    return cursor, mariadb_connection

if __name__ == '__main__':
    app.debug = True
    app.run(host = myhost, port = myport)
