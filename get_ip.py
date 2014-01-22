#!/usr/bin/python
"""

Author: Jared R. Luellen
This repo is located at: https://github.com/jluellen/sms_ip
Sends current internal and external IP on boot
Add to cron by: sudo crontab -e
Append: @reboot python /home/pi/get_ip.py &
Save crontab
Reboot device and test

"""


from googlevoice import Voice
import re
import os
import subprocess
import mechanize


voice = Voice()

def main():
	version = get_os()
	internal_ip = get_internal_ip(version)
	external_ip = get_external_ip()
	text = 'Raspberry Pi: \r\r' + 'Internal: ' + internal_ip + '\n' + 'External: ' + external_ip 
	print text
	send_text(text)

def get_os():
	# Determine which OS distribution the system is running
	version = os.uname()[0]
	return version

def get_internal_ip(version):
	if version == 'Darwin':
		internal_ip = subprocess.check_output(['/sbin/ifconfig','en0'])
		print internal_ip
		internal_ip = re.search('inet ([\d\.]*)', internal_ip)
	if version == 'Linux':
		internal_ip = subprocess.check_output(['/sbin/ifconfig','eth0'])
		internal_ip = re.search('inet addr:([\d\.]*)', internal_ip)
	internal_ip = internal_ip.group(1)
	return internal_ip

def get_external_ip():
	# Generates a web browser instance 
	# Opens www.whatsmyip.com/ and gets external IP address
	br = mechanize.Browser()

	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)

	# Follows refresh 0 but not hangs on refresh > 0
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	# User-Agent makes the destination website think it's from a real person
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	html = br.open('http://www.whatismyip.com/')
	html = html.read()
	html = unicode(html, errors='ignore')

	# Searches through the raw html file and grabs the paragraph "the-ip", where the external IP is displayed 
	match = re.search('<div class="the-ip">(.*)</div>', html)
	# Looks at "the-ip" section and finds html char, i.e. '&#58' 
	if match:
		chars = re.findall('\&\#(\d*)', match.group(1))
		external_ip = ''.join([chr(int(char)) for char in chars])
		#debug.write(str(external_ip))
		return external_ip

def send_text(text):
	# Reads a file listed in git ignore, it contains username, password, and phone number(s) you wish to send to
	# EXAMPLE user_info.txt file:
	# email@gmail.com
	# YOUR_PASSWORD
	# 3333333333, 3333333333, 3333333333
	user_info = open('/home/pi/sms_ip/user_info.txt', 'r')
	user_name = user_info.readline()
	user_pass = user_info.readline()
	user_tele = user_info.readline()
	user_info.close()
	voice.login(user_name, user_pass)
	phoneNumber = user_tele
	voice.send_sms(phoneNumber, text)


if __name__ == "__main__": main()