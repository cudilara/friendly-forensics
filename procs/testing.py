#!/usr/bin/env python

import requests, sys

url = "http://127.0.0.1:4000/varlog/"
txtpath = "../raw_files/varlog.txt"

varlogDict = {}


def read_file():
    try:
        parsedDict = None
        f = open(txtpath, 'r')
        for line in f:
            parsedDict = parse_line(line)
            if not parsedDict:
                continue
            print("Dictionary is ", parsedDict)
            send_data(line, url)
        f.close()
        return parsedDict
    except:
        print("Failed to process the file.")
        return None


def send_data(mydata, url):
    try:
        url = url + mydata
        print("HERE ", url)
        requests.post(url=url + mydata)
        print("Sent file line.")
    except:
        print("Failed to post to the server.")


def parse_line(line):
    line_arr = line.split()
    if len(line_arr) < 9:
        return None
    else:
        varlogDict = {
            'filePerms': line_arr[0],
            'linkNum': line_arr[1],
            'ownerName': line_arr[2],
            'ownerGroup': line_arr[3],
            'filesize': line_arr[4],
            'monthModified': line_arr[5],
            'dayModified': line_arr[6],
            'timeModified': line_arr[7],
            'dirName': line_arr[8]
        }
        return varlogDict


def main():
    parsedDict = read_file()
    if parsedDict != None:
        send_data(parsedDict, url)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
