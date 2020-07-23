import os
def sendEmail(sender,target,subject,body):
	f = open("email.txt","w")
	cmd = "MAIL FROM:" + sender + "\nRCPT TO:" + target + "\ndata\n" + "subject: " + subject + "\n\n" + body + "\n.\n"
	f.write(cmd)
	f.close()
	os.system("telnet studio.lrd.com 25 < email.txt")
	os.system("rm email.txt")
	return "sent"
