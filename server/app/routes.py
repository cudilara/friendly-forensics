#!/usr/bin/env python


from flask import render_template, Flask, logging
import pymysql

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

upload_location = '.'
app = Flask(__name__)
myhost = '0.0.0.0'
myport = 4001
Root, Passwd, DBname = 'root', 'password', 'forensic_data'
investigationID = 2

class DNS:
    domain = ''
    nameserver = ''
    insData = None

dns = DNS()
dns.insData = []

class Hosts:
    hostAddress = ''
    hostName = ''
    hData = None

myHosts = Hosts()
myHosts.hData = []

class InstalledPrograms:
    installed = None

progr = InstalledPrograms()
progr.installed = []

class IP:
    info = None

geoIP = IP()
geoIP.info = []

class LastLogin:
    lastLogsData = None

login = LastLogin()
login.lastLogsData = []

class Shadow:
    pinfo = None

pswd = Shadow()
pswd.pinfo = []

class SystemInfo:
    info = None

sysinfo = SystemInfo()
sysinfo.info = []

@app.route('/')
def my_form():
    return render_template('basic.html')


@app.route('/dns_servers/<msg>', methods=['POST', 'GET'])
def dns_servers(msg):
    if msg is None:
        logger.debug('Did not receive dns data.')
        return render_template('basic.html')
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        logger.debug('Failed to connect to the database.')
        return render_template('basic.html')
    arr = msg.split('20%')
    myarr = msg.split(' ')
    if myarr[0] == "domain":
        dns.domain = myarr[1]
        dns.domain = dns.domain.split('\n')[0]
        dns.insData.append(dns.domain)
    if myarr[0] == "nameserver":
        dns.nameserver = myarr[2]
        dns.insData.append(dns.nameserver)
    if len(dns.insData) == 2:
        dnssql = "INSERT INTO DNS(domain,nameserver,Investigations_id_investigation) VALUES(%s, %s, %s)"
        dns.insData.append(investigationID)
        db_cursor.execute(dnssql, dns.insData)
        db_connection.commit()
    db_connection.close()
    return render_template('basic.html', bodyText="")

@app.route('/hosts/<msg>', methods=['POST', 'GET'])
def hosts(msg):
    if msg is None:
        logger.debug('Did not receive hosts data.')
        return render_template('basic.html')
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        logger.debug('Failed to connect to the database.')
        return render_template('basic.html')
    arr = msg.split('\n')
    myarr = arr[0].split('\t')
    if len(myarr) >= 2:
        if myarr[0] != u'':
            myHosts.hostAddress = str(myarr[0])
        if myarr[1] != u'':
            myHosts.hostName = str(myarr[1])
        if len(myarr) > 2 and myarr[2] != "":
            myHosts.hostName = str(myarr[2])
    hostsql = "INSERT INTO Hosts(hostAddress,hostName,Investigations_id_investigation) Values(%s, %s, %s)"
    myHosts.hData.append(myHosts.hostAddress)
    myHosts.hData.append(myHosts.hostName)
    myHosts.hData.append(investigationID)
    try:
        db_cursor.execute(hostsql, myHosts.hData)
        db_connection.commit()
    except:
        # TODO handle this case
        logger.debug('Failed to send Hosts data to database.')
    myHosts.hData = []
    db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/installed/<msg>', methods=['POST', 'GET'])
def installed(msg):
    if msg is None:
        logger.debug('Did not receive installed programs data.')
        return render_template('basic.html')
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        logger.debug('Failed to connect to the database.')
        return render_template('basic.html')
    arr = msg.split('\n')
    installedsql = "INSERT INTO InstalledPrograms(programName,Investigations_id_investigation) Values(%s, %s)"
    installedProgr = str(arr[0])
    progr.installed.append(installedProgr)
    progr.installed.append(investigationID)
    try:
        db_cursor.execute(installedsql, progr.installed)
        db_connection.commit()
        progr.installed = []
    except:
        # TODO handle this case
        print('Failed to send Installed Programs data to database.')
    db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/ip_addresses_geo/<msg>', methods=['POST', 'GET'])
def ip_addresses_geo(msg):
    if msg is None:
        logger.debug('Did not receive geo ip data.')
        return render_template('basic.html')
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        logger.debug('Failed to connect to the database.')
        return render_template('basic.html')
    arr = msg.split('\n')
    hasDigit = any(i.isdigit() for i in arr[0])
    if hasDigit:
        geoIP.info.append(str(arr[0]))
    else:
        countryArr = (str(arr[0])).split(',')
        geoIP.info.append(str(countryArr[1]))
    if len(geoIP.info) == 2:
        geoIP.info.append(investigationID)
        sql = "INSERT INTO GeoIP(ip,country,Investigations_id_investigation) Values(%s, %s, %s)"
        db_cursor.execute(sql, geoIP.info)
        db_connection.commit()
        geoIP.info = []
    db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/last_logins/<msg>', methods=['POST', 'GET'])
def last_logins(msg):
    if msg is None:
        logger.debug('Did not receive last logins data.')
        return render_template('basic.html')
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        logger.debug('Failed to connect to the database.')
        return render_template('basic.html')
    arr = msg.split('\n')
    arr = [str(item) for item in arr]
    if len(arr) < 1:
        return render_template('basic.html', bodyText="")
    loginLine = arr[0].split(' ')
    loginLine = [var for var in loginLine if var]
    if len(loginLine) < 4:
        return render_template('basic.html', bodyText="")
    usr = loginLine[0]
    if usr == "wtmp":
        return render_template('basic.html', bodyText="")
    if loginLine[1] == "system":
        date = loginLine[6] + loginLine[5] + loginLine[7]
        endDate = loginLine[9]
    else:
        if loginLine[2] == ":0":
            date = loginLine[5] + loginLine[4] + loginLine[6]
            endDate = loginLine[8]
        else:
            date = loginLine[4] + loginLine[3] + loginLine[5]
            endDate = loginLine[7]
    sql = "INSERT INTO LastLogins(user,start,end,Investigations_id_investigation) Values(%s, %s, %s, %s)"
    login.lastLogsData.append(str(usr))
    login.lastLogsData.append(str(date))
    login.lastLogsData.append(str(endDate))
    login.lastLogsData.append(investigationID)
    db_cursor.execute(sql, login.lastLogsData)
    db_connection.commit()
    db_connection.close()
    login.lastLogsData = []
    return render_template('basic.html', bodyText="")


@app.route('/logins/<msg>', methods=['POST', 'GET'])
def logins(msg):
    return render_template('basic.html', bodyText="")


@app.route('/ls_filesys_etc/<msg>', methods=['POST', 'GET'])
def ls_filesys_etc(msg):
    return render_template('basic.html', bodyText="")


@app.route('/ls_filesys_dev/<msg>', methods=['POST', 'GET'])
def ls_filesys_dev(msg):
    return render_template('basic.html', bodyText="")


@app.route('/ls_filesys_home/<msg>', methods=['POST', 'GET'])
def ls_filesys_home(msg):
    return render_template('basic.html', bodyText="")


@app.route('/number_of_users/<msg>', methods=['POST', 'GET'])
def number_of_users(msg):
    return render_template('basic.html', bodyText="")


@app.route('/os_type/<msg>', methods=['POST', 'GET'])
def os_type(msg):
    if msg is None:
        logger.debug('Did not receive os data.')
        return render_template('basic.html')
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        logger.debug('Failed to connect to the database.')
        return render_template('basic.html')
    arr = msg.split('\n')
    myarr = arr[0].split('\t')
    myarr = myarr[0].split(' ')
    kernelName = myarr[0]
    machineName = myarr[1]
    kernelVersion = myarr[2]
    kVersionBuild = myarr[3] + " " + myarr[4] + " " + myarr[5] + " " + myarr[6] + " " + myarr[7] + " " + myarr[8] + " " + " " + myarr[9] + " " + myarr[10]
    processor = myarr[11]
    os = myarr[12] + " " + myarr[13]
    infosql = "INSERT INTO systeminfo(kernelName,machineName,kernelVersion,kVersionBuild,processor,os,Investigations_id_investigation) Values(%s, %s, %s, %s, %s, %s, %s)"
    sysinfo.info.append(kernelName)
    sysinfo.info.append(machineName)
    sysinfo.info.append(kernelVersion)
    sysinfo.info.append(kVersionBuild)
    sysinfo.info.append(processor)
    sysinfo.info.append(os)
    sysinfo.info.append(investigationID)
    try:
        db_cursor.execute(infosql, sysinfo.info)
        db_connection.commit()
    except:
        print("Did not insert system info into database.")
    print("HERE ", sysinfo.info)
    sysinfo.info = []
    db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/passwords/<msg>', methods=['POST', 'GET'])
def passwords(msg):
    if msg is None:
        logger.debug('Did not receive passwords data.')
        return render_template('basic.html')
    normalStr = msg.replace("_RRR_", "/")
    print(normalStr)
    myarr = normalStr.split(':')
    #TODO: figure out if we need this at all.
    return render_template('basic.html', bodyText="")


@app.route('/shadow/<msg>', methods=['POST', 'GET'])
def shadow(msg):
    if msg is None:
        logger.debug('Did not receive shadow data.')
        return render_template('basic.html')
    db_cursor, db_connection = connect_to_db(Root, Passwd, DBname)
    if db_cursor is None or db_connection is None:
        logger.debug('Failed to connect to the database.')
        return render_template('basic.html')
    normalStr = msg.replace("_RRRR_", ".")
    normalStr = normalStr.replace("_RRR_", "$")
    normalStr = normalStr.replace("_RR_", "/")
    myarr = normalStr.split(':')
    pswd.pinfo.append(myarr[0])
    pswd.pinfo.append(myarr[1])
    pswd.pinfo.append(investigationID)
    #TODO: make a dictionary that stores decrypted hashes for easy lookup.
    sql = "INSERT INTO Password(username,hash,Investigations_id_investigation) Values(%s, %s, %s)"
    try:
        db_cursor.execute(sql, pswd.pinfo)
        db_connection.commit()
    except:
        print("Did not insert shadow into database.")
    pswd.pinfo = []
    db_connection.close()
    return render_template('basic.html', bodyText="")


@app.route('/programs/<msg>', methods=['POST', 'GET'])
def programs(msg):
    return render_template('basic.html', bodyText="")


@app.route('/starting_programs/<msg>', methods=['POST', 'GET'])
def starting_programs(msg):
    return render_template('basic.html', bodyText="")


@app.route('/varlog/<msg>', methods=['POST', 'GET'])
def varlog(msg):
    return render_template('basic.html', bodyText="")


@app.route('/varlog_ls/<msg>', methods=['POST', 'GET'])
def varlog_ls(msg):
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
        logger.debug('Failed to connect to db.')
    return cursor, mariadb_connection


def insert(cursor):
    ins = "insert into varlog values(?, ?, ?, ?, ?, ?, ?, ?), []"
    cursor.execute(ins)

if __name__ == '__main__':
    app.debug = True
    app.run(host = myhost, port = myport)
