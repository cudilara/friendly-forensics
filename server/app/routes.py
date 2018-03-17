#!/usr/bin/env python


from flask import render_template, Flask
import pymysql

upload_location = '.'
app = Flask(__name__)
myhost = '0.0.0.0'
myport = 4001
Root, Passwd, DBname = 'root', 'password', 'forensic_data'

class DNS:
    domain = ''
    nameserver = ''
    insData = None

dns = DNS()
dns.insData = []



@app.route('/')
def my_form():
    return render_template('basic.html')


@app.route('/dns_servers/<msg>', methods=['POST', 'GET'])
def dns_servers(msg):
    if msg is None:
        print("Did not receive any message.")
        return render_template('basic.html')
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        print("Failed to connect to the database.")
        return render_template('basic.html')
    arr = msg.split('20%')
    myarr = arr[0].split(' ')
    if myarr[0] == "domain":
        dns.domain = myarr[1]
        dns.domain = dns.domain.split('\n')[0]
        dns.insData.append(dns.domain)
    if myarr[0] == "nameserver":
        dns.nameserver = myarr[2]
        dns.insData.append(dns.nameserver)
    if len(dns.insData) == 2:
        sql = "select * from Investigations"
        db_cursor.execute(sql)
        results = db_cursor.fetchall()
        print("Investigations: ", results)
        db_connection.commit()
        db_connection.close()
    return render_template('basic.html', bodyText="")

@app.route('/hosts/<msg>', methods=['POST', 'GET'])
def hosts(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/installed/<msg>', methods=['POST', 'GET'])
def installed(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/kernel_level/<msg>', methods=['POST', 'GET'])
def kernel_level(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/last_logins/<msg>', methods=['POST', 'GET'])
def last_logins(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/logins/<msg>', methods=['POST', 'GET'])
def logins(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/ls_filesys_etc/<msg>', methods=['POST', 'GET'])
def ls_filesys_etc(msg):
    # db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    # ls_filesys_parse(msg)
    # insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/ls_filesys_dev/<msg>', methods=['POST', 'GET'])
def ls_filesys_dev(msg):
    # db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    # ls_filesys_parse(msg)
    # insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/ls_filesys_home/<msg>', methods=['POST', 'GET'])
def ls_filesys_home(msg):
    # db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    # ls_filesys_parse(msg)
    # insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/number_of_users/<msg>', methods=['POST', 'GET'])
def number_of_users(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/os_type/<msg>', methods=['POST', 'GET'])
def os_type(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/programs/<msg>', methods=['POST', 'GET'])
def programs(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/starting_programs/<msg>', methods=['POST', 'GET'])
def starting_programs(msg):
    #db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    #filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/varlog/<msg>', methods=['POST', 'GET'])
def varlog(msg):
    # db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    # filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    # #insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/varlog_ls/<msg>', methods=['POST', 'GET'])
def varlog_ls(msg):
    # db_cursor, db_connection = connect_to_db('root', 'password', 'forensic_data')
    # filePerm, linkNum, ownerName, ownerGroup, filesize, modifTime, fileName = varlog_parse(msg)
    # insert(db_cursor)
    # db_connection.commit()
    # db_connection.close()
    return render_template('basic.html', bodyText="")


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
