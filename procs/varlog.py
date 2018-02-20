import os, subprocess, time

path = '/var/log'
writeFile = open('varlog.txt', 'wb')
for root, dirs, files in os.walk(path):
    for subdir in dirs:
        dirpath = os.path.join(root, subdir)
        proc = subprocess.check_output(["sudo", "ls", "-al", dirpath])
        if proc is not None:
            writeFile.write(str(proc))
writeFile.close()
