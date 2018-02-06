import os, subprocess, time
paths = ['/home', '/etc', '/dev']

for directory in paths:
	s = directory[1:]
	writeFile = open('ls_filesys_%s.txt' % s, 'wb')
	for root, dirs, files in os.walk(directory):
		for subdir in dirs:
			dirpath = os.path.join(root, subdir)
			proc = subprocess.check_output(["sudo", "ls", "-al", dirpath])
			if proc is not None:
				writeFile.write(str(proc))
	writeFile.close()
