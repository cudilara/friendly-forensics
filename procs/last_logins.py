import os

os.system('last -f /var/log/wtmp > ../raw_files/last_logins.txt')