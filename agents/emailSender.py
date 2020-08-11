import os
from base64 import b64encode
def sendEmail(sender,target,subject,body,pwd="password"):
	f = open("email.txt","w")
	cmd = "EHLO there\nAUTH PLAIN " + b64encode(b'\x00' + sender.encode() + b'\x00' + pwd.encode()).decode() + '\n' + "MAIL FROM:" + sender + "\nRCPT TO:" + target + "\ndata\n" + "subject: " + subject + "\n\n" + body + "\n.\n"
	f.write(cmd)
	f.close()
	os.system("telnet studio.lrd.com 587 < email.txt")
	os.system("rm email.txt")
	return "sent"

def getIP():
    os.system("ifconfig | grep inet | awk -F' ' '{print $2}' | head -n 1 > .ip")
    f = open(".ip","r")
    ip = f.read().strip()
    f.close()
    return ip

sendEmail("s" + getIP() + "@example.com","info@example.com","test","init")
