import os #Allows using bash commands from within python for accessing the email server.
from base64 import b64encode #To create the base 64 auth string.
def sendEmail(sender: str,target: str,subject: str,body: str,pwd="password")->str:
	"""
	Sends an email from sender to target by telneting into an SMTP (Simple Mail Transfer Protocol) server. Requires the server to allow pipelining for unauthenticated users.

	args:
		sender (str): The user sending the email. Must include the domain used for the addresses on the server.
		target (str): The intended recipient of the email. Must include the comain used for the addresses on the server.
		subject (str): the subject line of the email.
		body (str): the body of the email.
		pwd (str): The password to the account with username sender. Default value of "password".
	returns:
		str: A confirmation message that the function has completed.
	"""
	#Open a file labeled "email.txt" and write the SMTP commands required to send the email into it.
	f = open("email.txt","w")
	cmd = "EHLO there\nAUTH PLAIN " + b64encode(b'\x00' + sender.encode() + b'\x00' + pwd.encode()).decode() + '\n' + "MAIL FROM:" + sender + "\nRCPT TO:" + target + "\ndata\n" + "subject: " + subject + "\n\n" + body + "\n.\n"
	f.write(cmd)
	f.close()
	#Opens a telnet connection to the email server and reads lines from email.txt instead of stdin. Change the second argument to telnet on this line if the email server has a different hostname or domain.
	os.system("telnet studio.lrd.com 587 < email.txt")
	#Removes the now extraneous email.txt file.
	os.system("rm email.txt")
	#Returns a confirmation message.
	return "sent"

def getIP()->str:
    """
    Gets the IPv4 address of the VM running this script. Requires the VM to have the net-tools package installed.

    returns:
    	str: the IPv4 address of the local machine.
    """
    #Get the IPv4 address and redirect to ".ip".
    os.system("ifconfig | grep inet | awk -F' ' '{print $2}' | head -n 1 > .ip")
    #Open ".ip".
    f = open(".ip","r")
    #Read the IP address from ".ip" and remove any trailing whitespace.
    ip = f.read().strip()
    #close the ".ip" file.
    f.close()
    #return the content of ".ip".
    return ip

#This line calls sendEmail() to send an email from the address "s[ip]@example.com" to "info@example.com". The message will have the subject line "test" and consist of the word "init".
sendEmail("s" + getIP() + "@example.com","info@example.com","test","init")
