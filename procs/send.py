#!/usr/bin/env python
import requests, sys, os

# This program reads raw_files directory,
# parses the results,
# and sends them to the server.

url = "http://127.0.0.1:4000/"
procFolder = "../procs/"
outputFolder = "../raw_files/"
ext = ".txt"
txtPaths = ["varlog", "ls_filesys_dev", "ls_filesys_etc", "ls_filesys_home"]
parsedDict = None

def send_data(mydata, filename):
    try:
        print(url, filename, mydata)
        myurl = url + filename + mydata
        requests.post(url=myurl + mydata)
        print("Sent file line.")
    except:
        print("Failed to send to the server.")

def send_ls_filesys(file):
    for line in file:
        line_arr = line.split()
        if len(line_arr) < 9:
            continue
        else:
            send_data(line, "ls_filesys/")

def send_varlog(file):
    for line in file:
        line_arr = line.split()
        if len(line_arr) < 9:
            continue
        else:
            send_data(line, "varlog/")


def main():
    for filename in txtPaths:
        try:
            mypath = outputFolder + filename + ext
            f = open(mypath, 'r')
            if filename == "varlog":
                send_varlog(f)
            elif filename == "ls_filesys_dev" or filename == "ls_filesys_etc" or filename == "ls_filesys_home":
                send_ls_filesys(f)
            f.close()
        except:
            print("Failed to process the file ", filename)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
