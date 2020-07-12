#!/usr/bin/env python3

import os, sys # TODO: use subprocess instead of os (?)

# Test payload information
# Design considerations: 
#	Include entire payload in worm (CE preference), or have worm reach out to download payload from server
payload_name = 'test_payload'
payload_content = "print('Hello World')"

# Creates a copy of the payload on host
def copy_payload():
	try:
		f = open(payload_name,'x') # 'x' opens for exclusive creation, failing if the file already exists
		f.write(payload_content)
		f.close()
	except:
		# This current way of checking if a host has been infected is not robust enough
		print(f'{payload_name} already exists!')
		sys.exit(0)

# Executes payload on host
def execute_payload():
	exec(open(payload_name).read())
	#os.chmod(payload_name, 0o744) # Changes permissions to: -rwxr--r--

def main():
	copy_payload()
	execute_payload()

	# Rudimentary way to make a LOCAL copy of itself when executed
	script = sys.argv
	name = script[0] # type: string

	os.mkdir('test')
	os.system('cp ' + name + ' test')

	"""
	Making a copy of itself on vulnerable host:
	1) Identify RCE vulnerability
	2) Bring this script to host using RCE vulnerability (eg. echo [contents] > /tmp/worm)
	3) Execute /tmp/worm on vulnerable host
	4) This will propagage
	"""

main()
