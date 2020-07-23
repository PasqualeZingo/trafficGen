import os
def sendEmail(sender,target,body):
	f = open("email.txt","w")
	cmd = "MAIL FROM:" + sender + "\nRCPT TO:" + target + "\ndata\n" + body + "\n.\n"
	f.write(cmd)
	f.close()
	os.system("telnet studio.lrd.com 25 < email.txt")
	os.system("rm email.txt")
	return "sent"

print(sendEmail("God","sales@example.com","init"))
