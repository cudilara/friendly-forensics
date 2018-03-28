import os

# DNS servers
os.system('cat /etc/resolv.conf > ../raw_files/dns_servers.txt')

# Host names
os.system('cat /etc/hosts > ../raw_files/hosts.txt')

# Number of users
os.system('users | wc -w > ../raw_files/number_of_users.txt')

# Installed software
os.system('dpkg --get-selections | cut -f1 > ../raw_files/installed.txt')

# Installed programs
os.system('ls /usr/sbin/ > ../raw_files/programs.txt')

# Programs starting on boot
os.system('ls /etc/init.d > ../raw_files/starting_programs.txt')

# Last logins
os.system('last -f /var/log/wtmp > ../raw_files/last_logins.txt')

# Logins
os.system('sudo cp /var/log/auth.log ../raw_files/logins.txt')

# Type of OS
os.system('uname -a > ../raw_files/os_type.txt')
# TODO: remove hashtag in output, replace slash at the end with space

# Available logs
os.system('ls /var/log > ../raw_files/varlog_ls.txt')

# IP addresses
os.system('netstat -vatn | awk \'{print $5}\' > ../raw_files/ip_addresses.txt')
rfile = open("../raw_files/ip_addresses.txt", "r")
wfile = open("../raw_files/ip_addresses_geo.txt", "w")
toWrite = ""
for line in rfile:
    hasDigit = any(i.isdigit() for i in line)
    if hasDigit and "0.0.0.0" not in line:
        ip = line.split(':')[0]
        geoRes = os.popen('geoiplookup ' + ip).read()
        res = line + str(geoRes)
        toWrite = toWrite + res
wfile.write(toWrite)
rfile.close()
wfile.close()

# Passwords
os.system('cat /etc/passwd > ../raw_files/passwords.txt')
# TODO: replace slashes with _RRR_

# Shadow
# TODO: replace . with _RRRR_
# TODO: replace $ with _RRR_
# TODO: replace / with _RR_
# try:
#	os.system('cat /etc/shadow > ../raw_files/shadow.txt')
# except:
#	print("Did not get /etc/shadow")
