#!/usr/bin/env python
from flask import render_template, request, Flask
import pymysql
import datetime
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

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
    investName, investId = insert_user_investigation_name(db_cursor, db_connection)
    dnsResults = get_dns_data(db_cursor, investId)
    addrRes, nameRes, hostL = get_hosts_data(db_cursor, investId)
    programsResults1, programsResults2, programsResults3, programsResults4, programsResults5 = get_installed_programs(db_cursor)
    kernelName, machineName, kernelVersion, kVersionBuild, processor, os = get_system_info(db_cursor, investId)
    hostsName, hostsPassword = get_shadow_data(db_cursor, investId)
    IP, country = get_geo_ip(db_cursor, investId)
    db_connection.close()
    return render_template('basic.html', bodyText=bodyText, DNSoutput=dnsResults, IP=IP, country=country, NameInPswd=hostsName, hostsPassword=hostsPassword, acceptedName=investName, kernelName=kernelName, machineName=machineName, kernelVersion=kernelVersion, kVersionBuild=kVersionBuild, processor=processor, os=os,  hostsAddress=addrRes, hostsName=nameRes, allPrograms1=programsResults1, allPrograms2=programsResults2, allPrograms3=programsResults3, allPrograms4=programsResults4, allPrograms5=programsResults5)


def get_geo_ip(db_cursor, investId):
    sql = "select ip, country from GeoIP"
    db_cursor.execute(sql)
    results = db_cursor.fetchall()
    IP, country = [], []
    for tuple in results:
        IP.append(str(tuple[0]))
        country.append(str(tuple[1]))
    return IP, country


def get_shadow_data(db_cursor, investId):
    sql = "select username, hash from Password"
    try:
        db_cursor.execute(sql)
        results = db_cursor.fetchall()
    except:
        results = "Did not get data for passwords."
    username, password = [], []
    for tuple in results:
        name = tuple[0]
        pswd = tuple[1]
        if pswd == "*":
            pswd = "no password"
        if name not in username:
            username.append(name)
            password.append(pswd)
    return username, password


def get_system_info(db_cursor, investId):
    sql = "select kernelName, machineName, kernelVersion, kVersionBuild, processor, os from systemInfo where Investigations_id_investigation = %s"
    try:
        retVal = ""
        db_cursor.execute(sql, investId)
        results = db_cursor.fetchall()
        if len(results) > 1:
            retVal = results[0]
            retValSet = set(retVal)
            for res in results:
                setRes = set(res)
                if setRes != retValSet:
                    retVal.append(res)
        return retVal[0], retVal[1], retVal[2], retVal[3], retVal[4], retVal[5]
    except:
        retVal = "No System data."
        return retVal, retVal, retVal, retVal, retVal, retVal


def insert_user_investigation_name(db_cursor, db_connection):
        investigationName = request.form['investigation_name']
        now = datetime.datetime.now()
        checkSQL = "select id_investigation, name_investigation from Investigations"
        db_cursor.execute(checkSQL)
        names = db_cursor.fetchall()
        for n in names:
            investName = n[1]
            investId = n[0]
            if investigationName == investName:
                return investigationName, investId
        ins = "INSERT INTO Investigations(name_investigation,date_investigation) VALUES(%s, %s)"
        values = investigationName, now
        try:
            db_cursor.execute(ins, values)
            db_connection.commit()
        except:
            print("Did not insert investigation name.")
        getSQL = "select id_investigation from Investigations where name_investigation = %s"
        db_cursor.execute(getSQL, investigationName)
        id = db_cursor.fetchall()
        return investigationName, id[0][0]


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
        if addr not in addresses and name not in names:
            addresses.append(addr)
            names.append(name)
            hostLength += 1
    return addresses, names, hostLength

def get_installed_programs(db_cursor):
    sql = "select programName from InstalledPrograms"
    try:
        db_cursor.execute(sql)
        installedPrograms = db_cursor.fetchall()
    except:
        installedPrograms = "Failed to retrieve installed programs."
    programName = []
    for pr in installedPrograms:
        st = pr[0]
        if st not in programName:
            programName.append(st)
    length = len(programName) / 5
    doubleL = length * 2
    tripleL = length * 3
    quadrupleL = length * 4
    programs1 = programName[0:length]
    programs2 = programName[length:doubleL]
    programs3 = programName[doubleL:tripleL]
    programs4 = programName[tripleL:quadrupleL]
    programs5 = programName[quadrupleL:]
    return programs1, programs2, programs3, programs4, programs5

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
