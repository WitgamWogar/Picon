import xml.dom.minidom, os, paramiko, time, subprocess, sys
from progress.bar import Bar


cip = raw_input("Current IP:: ")
subnet = raw_input("Enter Subnet:: ")
ip = raw_input("Enter Last Digits of IP:: ")
hostname = raw_input("Enter Hostname:: ")
gateway = raw_input("Enter Gateway:: ")
aetype = raw_input("slack or safe or board?:: ")
ssid = raw_input("SSID:: ")
netpass = raw_input("Wifi Password:: ")
ssid = ssid.encode('hex')
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



if aetype == "slack":
	autoex_l = '/home/tyler/Desktop/PIconfig/AEslack/autoexec.py'
	print "This Device is now setup for Slackline"
elif aetype == "safe": 
	autoex_l = '/home/tyler/Desktop/PIconfig/AEsafe/autoexec.py'
	print "This Device is now setup for Safety Video"
else: 
	autoex_l = '/home/tyler/Desktop/PIconfig/board/autoexec.py'
	print "This Device is now setup for Safety Video"
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



sftp = ssh.open_sftp()
remotehost = cip
cmd = "arp -a"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
output, errors = p.communicate()
if output is not None :
    if sys.platform in ['linux','linux2']:
        for i in output.split("\n"):
            if remotehost in i:
                for j in i.split():
                    if ":" in j:
                        macadd = j
    elif sys.platform in ['win32']:
        item =  output.split("\n")[-2]
        if remotehost in item:
            macadd = item.split()[1]
macadd = macadd.replace(':', '')
print macadd

configstr = '''[wifi_%s_%s_managed_wep]
	Name=Wifi
	SSID='''%(macadd, ssid) + ssid + '''
	Frequency=2437
	Favorite=true
	AutoConnect=true
	Modified=2013-10-04T20:36:43.505939Z
	Passphrase=mypassword
	IPv4.method=manual
	IPv6.method=off
	IPv6.privacy=disabled
	IPv4.netmask_prefixlen=24
	Nameservers=8.8.8.8;8.8.4.4;
	IPv4.local_address=192.168.''' + subnet + '.' + ip + '''
	IPv4.gateway=192.168.''' + subnet + '.' + gateway
f = open('settings.xml', 'w')
f.write(configstr)
f.close()
print "Settings have been changed, your videos are now uploading, please wait..."
networkpath = ".cache/connman/wifi_" + macadd + '_' + ssid + '_managed_wep/settings'
try:
	sftp.mkdir('.cache/connman/wifi_' + macadd + '_' + ssid + '_managed_wep')
except:
	pass
sftp.put(settingsfile, networkpath)
sftp.put(local_path, remote_path)
sftp.put(autoex_l, autoex_r)
sftp.put(local_vid1, remote_vid1)
sftp.put(local_vid2, remote_vid2)
sftp.put(local_vid3, remote_vid3)
sftp.put(local_vid4, remote_vid4)



print "Upload Complete, Rebooting..."
ssh.exec_command("reboot")
sftp.close()
ssh.close()
