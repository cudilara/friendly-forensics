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
    bodyText = "Easy Forensics"
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        print("Failed to connect to the database.")
        return render_template('basic.html', bodyText=bodyText)
    if request.form['investigation_name'] == "":
        return render_template('basic.html', bodyText=bodyText)
    insert_user_investigation_name(db_cursor, db_connection)
    investName, investId = get_investigation_name(db_cursor)
    investigationTitle = "Data for investigation: " + investName
    dnsResults = get_dns_data(db_cursor, investId)
    addrRes, nameRes, hostL = get_hosts_data(db_cursor, investId)
    hostData = ("")
    for addr in addrRes:
        hostData = hostData + '\n' + addr
    programsResults = get_installed_programs(db_cursor)
    db_connection.close()
    return render_template('basic.html', bodyText=bodyText, acceptedName=investigationTitle, DNSoutput=dnsResults, hostsAddress=hostData, hostsName=nameRes)
    # return render_template('basic.html', bodyText=bodyText, acceptedName=investigationTitle, DNSoutput=dnsResults, hostsAddress=addrRes, hostsName=nameRes, hostLength=hostL, installedPrograms=programsResults)


def insert_user_investigation_name(db_cursor, db_connection):
        investigationName = request.form['investigation_name']
        now = datetime.datetime.now()
        ins = "INSERT INTO Investigations(name_investigation,date_investigation) VALUES(%s, %s)"
        values = investigationName, now
        try:
            db_cursor.execute(ins, values)
            db_connection.commit()
        except:
            #TODO find investigation with that name
            print("Could not insert into Investigations name ", investigationName)


def get_investigation_name(db_cursor):
    sql = "select id_investigation, name_investigation from Investigations where id_investigation=1"
    try:
        db_cursor.execute(sql)
        investigation = db_cursor.fetchall()
    except:
        investigation = "Failed to get investigations names from database."
    investName = investigation[0][1]
    investId = investigation[0][0]
    return investName, investId


def get_dns_data(db_cursor, investId):
    sql = "select domain, nameserver from DNS where Investigations_id_investigation = %s"
    try:
        retVal = ""
        db_cursor.execute(sql, investId)
        dnsResults = db_cursor.fetchall()
        if len(dnsResults) > 1:
            retVal = dnsResults[0]
            retValSet = set(retVal)
            for res in dnsResults:
                setRes = set(res)
                if setRes != retValSet:
                    retVal.append(res)
    except:
        retVal = ""
    if retVal != "":
        retVal = "DNS name: " + retVal[0] + "; IP address:" + retVal[1]
    return retVal

def get_hosts_data(db_cursor, investId):
    sql = "select hostAddress, hostName from Hosts where Investigations_id_investigation = %s"
    try:
        db_cursor.execute(sql, investId)
        hostResults = db_cursor.fetchall()
    except:
        hostResults = "Failed to get hosts data."
    addresses, names = [],[]
    hostLength = 0
    for tuple in hostResults:
        addr = tuple[0]
        name = tuple[1]
        addresses.append(addr)
        names.append(name)
        hostLength += 1
    return addresses, names, hostLength

def get_installed_programs(db_cursor):
    sql = "select * from InstalledPrograms"
    try:
        db_cursor.execute(sql)
        installedPrograms = db_cursor.fetchall()
    except:
        installedPrograms = "Failed to retrieve installed programs."
    return installedPrograms

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