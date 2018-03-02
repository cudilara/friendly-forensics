import os, subprocess, time

# Output meaning:
#
# file permissions,
# number of links,
# owner name,
# owner group,
# file size,
# time of last modification, and
# file/directory name

path = '/var/log'
writeFile = open('varlog.txt', 'wb')
for root, dirs, files in os.walk(path):
    for subdir in dirs:
        dirpath = os.path.join(root, subdir)
        try:
            proc = subprocess.check_output(["sudo", "ls", "-al", dirpath])
            if proc is not None:
                msgB = str.encode(str(proc))
                writeFile.write(msgB)
        except:
            failMsg = 'Failed to run command <sudo ls -al> on directory %s\n' % subdir
            msgB = str.encode(failMsg)
            writeFile.write(msgB)
writeFile.close()


