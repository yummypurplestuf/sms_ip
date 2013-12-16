#!/usr/bin/python
# Author: Jared R. Luellen
# Sends current IP address as sms to a phone number on boot
# Add to cron by: sudo crontab -e
# Append: @reboot python /home/pi/MyScript.py &
# Save crontab
# Reboot device and test

from googlevoice import Voice
#from googlevoice.util import input
import netifaces
import sys
import os


# netifaces is not a built in Python Library: easy_install netifaces
interfaces = netifaces.interfaces()
voice = Voice()
for i in interfaces:
    if i == 'lo':
        continue
    iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
    if iface != None:
        for j in iface:
            ip_addr = j['addr']
            connection = True

if connection == True:
	try:
		# Reads a file listed in git ignore, it contains username, password, and phone number(s) you wish to send to
		# EXAMPLE user_info.txt file:
		# email@gmail.com
		# YOUR_PASSWORD
		# 3333333333, 3333333333, 3333333333

		# MUST SET ABSOLUTE PATH FOR user_info.txt 
		user_info = open(str(os.getcwd())+'/user_info.txt', 'r')
		user_name = user_info.readline()
		user_pass = user_info.readline()
		user_tele = user_info.readline()
		user_info.close()
		voice.login(user_name, user_pass)
		phoneNumber = user_tele
		text = 'RaspberryPi\n\n'+'IP: '+str(ip_addr)
		print len(text)
	except:
		print 'failed to send IP'
		sys.exit(1)
	finally:
		voice.send_sms(phoneNumber, text)
