import os

file = '/var/log/auth.log'
os.system('sudo cp /var/log/auth.log ../raw_files/logins.txt')