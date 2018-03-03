import os, subprocess

paths = ['/home', '/etc', '/dev']

for directory in paths:
    dirName = directory[1:]
    writeFile = open('../raw_files/ls_through_%s.txt' % dirName, 'wb')
    for root, dirs, files in os.walk(directory):
        for subdir in dirs:
            dirpath = os.path.join(root, subdir)
            try:
                proc = subprocess.check_output(["ls", "-al", dirpath])
                if proc is not None:
                    msgB = str.encode(str(proc))
                    writeFile.write(msgB)
            except:
                failMsg = 'Failed to run command <ls -al> on directory %s\n' % subdir
                msgB = str.encode(failMsg)
                writeFile.write(msgB)
    writeFile.close()
