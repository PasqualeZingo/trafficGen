import os
from base64 import b64encode
def sendEmail(sender,pwd,target,subject,body):
	f = open("email.txt","w")
	cmd = "EHLO there\nAUTH PLAIN " + b64encode(b'\x00' + sender.encode() + b'\x00' + pwd.encode()).decode() + '\n' + "MAIL FROM:" + sender + "\nRCPT TO:" + target + "\ndata\n" + "subject: " + subject + "\n\n" + body + "\n.\n"
	f.write(cmd)
	f.close()
	os.system("telnet studio.lrd.com 587 < email.txt")
	os.system("rm email.txt")
	return "sent"
