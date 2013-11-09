import xml.dom.minidom, os, time, subprocess, sys, inspect
lib_path = os.path.abspath('lib')
sys.path.append(lib_path)
import paramiko

cip = raw_input("Current IP? ")
ip = raw_input("New IP? ")
hostname = raw_input("Hostname? ")
gateway = raw_input("Gateway? ")
ssid = raw_input("SSID:: ")
while True:
	security = raw_input("WPA or WEP?")
	security = security.lower()
	if security == "wpa" or security == "wep":
		break
	else:
		print("Please enter 'WPA' or 'WEP'")
if security == "wep":
	security = security
else:
	security = "psk"
netpass = raw_input("Wifi Password? ")
ssid = ssid.encode('hex')
remote_path = '.xbmc/userdata/advancedsettings.xml'
local_path = 'advancedsettings.xml'
settingsfile = "settings.xml"
filename='advancedsettings.xml'

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

configstr = '''[wifi_%s_%s_managed_%s]
Name=Wifi
SSID= %s
Frequency=2437
Favorite=true
AutoConnect=true
Modified=2013-10-04T20:36:43.505939Z
Passphrase=%s
IPv4.method=manual
IPv6.method=off
IPv6.privacy=disabled
IPv4.netmask_prefixlen=24
Nameservers=8.8.8.8;8.8.4.4;
IPv4.local_address=%s
IPv4.gateway=%s''' % (macadd, ssid, security, ssid, netpass, ip, gateway)


f = open('settings.xml', 'w')
f.write(configstr)
f.close()

networkpath = ".cache/connman/wifi_%s_%s_managed_%s/settings" % (macadd, ssid, security)
try:
	sftp.mkdir('.cache/connman/wifi_%s_%s_managed_%s' % (macadd, ssid, security))
except:
	pass
sftp.put(settingsfile, networkpath)
sftp.put(local_path, remote_path)
print "Complete, Rebooting..."
ssh.exec_command("reboot")
sftp.close()
ssh.close()
