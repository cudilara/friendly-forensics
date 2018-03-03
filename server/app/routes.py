#!/usr/bin/env python
from flask import render_template, request, Markup, Flask, redirect, url_for, json
import pymysql
pymysql.install_as_MySQLdb()

upload_location = '.'
app = Flask(__name__)
myhost = '0.0.0.0'
myport = 4000


# TODO: create user in db, password

@app.route('/')
def index():
    bodyText = "Welcome to Madinger's thesis project!"
    return render_template('basic.html', bodyText=bodyText)


@app.route('/varlog/<msg>', methods=['POST', 'GET'])
def varlog(msg):
    db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    db_connection.commit()
    db_connection.close()
    return render_template('basic.html', bodyText=bodyText)

@app.route('/ls_filesys/<msg>', methods=['POST', 'GET'])
def ls_filesys(msg):
    db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    ls_filesys_parse(msg)
    bodyText = "Hi"
    #insert(db_cursor)
    db_connection.commit()
    db_connection.close()
    return render_template('basic.html', bodyText=bodyText)

def varlog_parse(msg):
    no20 = msg.split('20%')
    arr = no20[0].split(' ')
    if len(arr) > 12:
        filePerm = arr[0]
        linkNum = arr[1]
        ownerName = arr[2]
        ownerGroup = arr[3]
        filesize = arr[8]
        modifTime = arr[9] + arr[10] + " " + arr[11]
        fileName = arr[12]
        return filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName

def ls_filesys_parse(msg):
    #TODO: this needs to be parsed correctly
    no20 = msg.split('20%')
    arr = no20[0].split(' ')
    if len(arr) > 10:
        filePerm = arr[0]
        linkNum = arr[2]
        ownerName = arr[3]
        ownerGroup = arr[4]
        filesize = arr[6]
        modifTime = arr[7] + arr[8] + " " + arr[9]
        fileName = arr[10]
        print("HERE ", filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName)

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
    app.run(host = myhost, port = myport)
