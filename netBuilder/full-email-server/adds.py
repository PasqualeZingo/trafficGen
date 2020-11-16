"""
This script is designed to add usable email addresses to the email server. It adds an address for every ip address for each ip address on the 192.168.1.0 subnet.
"""

f = open('addresses','r')
addrs = f.read()
f.close()

addrs = addrs.split('\n')

try: 
	f=open("passwd","x")
	f.close()
	f = open("login_maps","a")

	for a in addrs:
		f.write("%s\t%s\n" % (a, a))
	f.close()
	
	
	f = open('passwd','a')
	
	for a in addrs:
		f.write("%s:{PLAIN}password" % a)
	f.close()
	
	
	
	f = open('vmailbox','a')
	
	for a in addrs:
		f.write("%s\t%s/\n" % (a,"example.com/%s" % a.split('@')[0]))
	f.close()

except:
	f=open("passwd","a")
	for a in addrs:
		f.write("%s:{PLAIN}password\n" % a)
	f.close()

