# Author: Jared R. Luellen
# Sends current IP address as sms to a phone number on boot
# Add to cron by: sudo crontab -e
# Append: @reboot python /home/pi/MyScript.py &
# Save crontab
# Reboot device and test

from googlevoice import Voice
#from googlevoice.util import input
import sys
import mechanize # pip install mechanize
import re
import subprocess
import os

voice = Voice()
#debug = open('debug.txt','w')

# Determine which OS distribution the system is running
#version = os.uname()[0]
# Run different re.seach depending on the OS ('Darwin') is OSx
#if version == 'Darwin':
#internal_ip = subprocess.check_output(['ifconfig','en0'])
#internal_ip = re.search('inet ([\d\.]*)', internal_ip)
#if version == 'Linux':
internal_ip = subprocess.check_output(['ifconfig','eth0'])
internal_ip = re.search('inet addr:([\d\.]*)', internal_ip)
internal_ip = internal_ip.group(1)
#debug.write(str(internal_ip))
print internal_ip

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
	print external_ip

# Reads a file listed in git ignore, it contains username, password, and phone number(s) you wish to send to
# EXAMPLE user_info.txt file:
# email@gmail.com
# YOUR_PASSWORD
# 3333333333, 3333333333, 3333333333
user_info = open('user_info.txt', 'r')
user_name = user_info.readline()
user_pass = user_info.readline()
user_tele = user_info.readline()
user_info.close()
voice.login(user_name, user_pass)
phoneNumber = user_tele
text = 'Raspberry Pi:' +'\r\r'+'Internal:'+' '+internal_ip + '\n' + 'External:'+ ' '+external_ip

#debug.close()
voice.send_sms(phoneNumber, text)