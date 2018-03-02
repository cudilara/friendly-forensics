#!/usr/bin/env python
from flask import render_template, request, Markup, Flask, redirect, url_for, json
import pymysql
pymysql.install_as_MySQLdb()

upload_location = '.'
app = Flask(__name__)


# TODO: create user in db, password

@app.route('/')
@app.route('/varlog/<msg>', methods=['POST', 'GET'])
def varlog(msg):
    db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    bodyText = parse_str(msg)
    #insert(db_cursor)
    db_connection.commit()
    db_connection.close()
    return render_template('basic.html', bodyText=bodyText)


def parse_str(msg):
    arr1 = msg.split('20%')
    arr = arr1[0]
    filePerm = arr[0]
    linkNum = arr[1]
    ownerName = arr[2]
    ownerGroup = arr[3]
    filesize = arr[4]
    modifTime = arr[5] + arr[6] + arr[7]
    fileName = arr[8]
    print("HERE: ", filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName)


def connect_to_db(username, pswd, db):
    cursor = None
    mariadb_connection = None
    try:
        mariadb_connection = pymysql.connect(user=username, password=pswd, database=db)
        cursor = mariadb_connection.cursor()
    except:
        print("Failed to connect to db.")
    return cursor, mariadb_connection


def insert(cursor):
    ins = "insert into varlog values(?, ?, ?, ?, ?, ?, ?, ?), []"
    cursor.execute(ins)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 4000)
