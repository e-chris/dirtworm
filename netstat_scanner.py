#!/usr/bin/env python3
import subprocess
subprocess.call("netstat") #add any code you want to execute

# Seomthing more dynamic could be
# p = subprocess.Popen(["ping", "-c", "10", "ip/url"], stdout=subprocess.PIPE) => use to check other online systems or ping back to attacker to make sure victim's system is alive and well.
# output, err = p.communicate()
# print  output
