import os

os.system('uname -a > ../raw_files/os_type.txt')
os.system('uname -r > ../raw_files/kernel_level.txt')
os.system('users | wc -w > ../raw_files/number_of_users.txt')