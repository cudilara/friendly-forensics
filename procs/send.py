#!/usr/bin/env python
import requests, sys, os

# This program reads raw_files directory,
# parses the results,
# and sends them to the server.

url = "http://127.0.0.1:4001/"
procFolder = "../procs/"
outputFolder = "../raw_files/"
ext = ".txt"
# txtPaths = ["dns_servers", "hosts", "varlog", "ls_filesys_home", "number_of_users",
#             "installed", "programs", "starting_programs", "last_logins", "os_type", "kernel_level", "varlog_ls"]
txtPaths = []
# done: "dns_servers", "hosts", "installed", "os_type", "passwords", "shadow", "ip_addresses_geo"
#have404=["logins", "ls_filesys_dev", "ls_filesys_etc"]
parsedDict = None


def send_data(mydata, filename):
    myurl = ""
    try:
        myurl = url + filename + "/" + mydata
        requests.post(url=myurl + mydata)
    except:
        print("Failed to send to the server. ", myurl, " with data: ", mydata)


def main():
    for filename in txtPaths:
        try:
            mypath = outputFolder + filename + ext
            f = open(mypath, 'r')
            for line in f:
                if line != "":
                    send_data(line, filename)
            f.close()
        except:
            print("Failed to process the file ", filename)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
