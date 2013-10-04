import xml.dom.minidom
import os
import paramiko
import time
import subprocess
from progress.bar import Bar


cip = raw_input("Current IP:: ")
subnet = raw_input("Enter Subnet:: ")
ip = raw_input("Enter Last Digits of IP:: ")
hostname = raw_input("Enter Hostname:: ")
gateway = raw_input("Enter Gateway:: ")
aetype = raw_input("slack or safe?:: ")
local_path = '/home/tyler/Desktop/PIconfig/advancedsettings.xml'
remote_path = '.xbmc/userdata/advancedsettings.xml'
remote_vid1 = 'videos/GetAirSafetyVideo.mp4'
remote_vid2 = 'videos/Slackline.mp4'
remote_vid3 = 'videos/Slackline2.mp4'
remote_vid4 = 'videos/Slackline3.mp4'
autoex_r = '.xbmc/userdata/autoexec.py'
local_vid1 = '/home/tyler/Desktop/PIconfig/Videos/GetAirSafetyVideo.mp4'
local_vid2 = '/home/tyler/Desktop/PIconfig/Videos/Slackline.mp4'
local_vid3 = '/home/tyler/Desktop/PIconfig/Videos/Slackline2.mp4'
local_vid4 = '/home/tyler/Desktop/PIconfig/Videos/Slackline3.mp4'
settingsfile = "/home/tyler/Desktop/PIconfig/settings.xml"
filename='advancedsettings.xml'
networkpath = ".cache/connman/ethernet_b827eb286dd3_cable/settings"
configstr = '''[ethernet_b827eb286dd3_cable]
	Name=Wired
	AutoConnect=true
	Modified=1970-01-01T00:00:23.034072Z
	IPv4.method=manual
	IPv6.method=off
	IPv6.privacy=disabled
	IPv4.netmask_prefixlen=24
	Nameservers=8.8.8.8;8.8.4.4;
	IPv4.local_address=192.168.''' + subnet + '.' + ip + '''
	IPv4.gateway=192.168.''' + subnet + '.' + gateway

if aetype == "slack":
	autoex_l = '/home/tyler/Desktop/PIconfig/AEslack/autoexec.py'
else: 
	autoex_l = '/home/tyler/Desktop/PIconfig/AEsafe/autoexec.py'

print "Input taken, computing..."


server, username, password = (cip, 'root', 'openelec')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(server, username=username, password=password)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls /tmp')



doc = xml.dom.minidom.parse(filename)

def replace(tagname, newvalue):
	doc.getElementsByTagName(tagname)[0].childNodes[0].nodeValue = newvalue

replace('devicename', hostname)

f = open('settings.xml', 'w')
f.write(configstr)
f.close()
print "Settings have been changed, your videos are now uploading, please wait..."

sftp = ssh.open_sftp()
bar = Bar('Uploading files', max=6)
for i in range(6):
	sftp.put(local_path, remote_path)
	bar.next()
	sftp.put(autoex_l, autoex_r)
	bar.next()
	sftp.put(local_vid1, remote_vid1)
	bar.next()
	sftp.put(local_vid2, remote_vid2)
	bar.next()
	sftp.put(local_vid3, remote_vid3)
	bar.next()
	sftp.put(local_vid4, remote_vid4)
	bar.next()
	sftp.put(settingsfile, networkpath)
bar.finish()
print "Upload Complete, Rebooting..."
ssh.exec_command("reboot")
sftp.close()
ssh.close()
