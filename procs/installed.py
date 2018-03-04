import os

os.system('dpkg --get-selections | cut -f1 > ../raw_files/installed.txt')