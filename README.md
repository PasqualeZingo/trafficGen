# trafficGen
This is a mono repo containing everything needed to operate and develop on the virtualized network within brass.
## Prereqs
### VMWare Workstation
The UD College of Engineering provides a number of different softwares through UDeploy. Our development VM runs on VMware Workstation which can be downloaded from [UDeploy here](https://udeploy.udel.edu/software/vmware-for-university-of-delaware/)


### UD VPN
In order to connect to brass, you need to be connected to the UD network. [The UD AnyConnect VPN](https://udeploy.udel.edu/software/anyconnect-vpn/) can be found here. If you haven't already, the UD VPN also requires a second password, which is generated through google authenticator. You can set that up by following the instructions layed out on this [webpage](https://services.udel.edu/TDClient/32/Portal/KB/ArticleDet?ID=4)


### IDS-ML VM
Our VM image is hosted on google drive which can be downloaded here. #TODO insert vm image link

## Parts of this repo
* GNS3
* UserAgent
* ML

# Network setup
In order to generate traffic, you will need to have a virtual network with servers that the useragent can interact with. Currently, these consist of a print server, and an email server.

## Email server
This is perhaps the most difficult of the three servers to set up and configure. This server will allow the userAgent to send emails via telnet to predefined users after authentication. This tutorial assumes you already have a pfsense router with DNS configured. The template on brass will have the default domain luked.com, however, if the email server is named "studio", it will recieve a static ip of 192.168.1.1 and a unique domain of lrd.com. Keep this in mind when telneting into the server.

### Installation
The first step to setting up the server is to install the software that the server will use to relay the mail, along with other basic utilities. To do this, run the following command:

    apt-get update && apt-get install -y rsyslog telnet postfix dovecot-common dovecot-imapd dovecot-pop3d git
The postfix and dovecot packages are used for sending mail and authentication, respectively. Rsyslog simplifies troubleshooting postfix. Telnet is used to interact with the Simple Mail Transfer Protocol (SMTP for short) server for testing purposes.

### Postfix configuration
A clean postfix installation will have to config files within its directory at /etc/postfix. You will need to replace these files with the ones in netBuilder/postfix-conf in this repo. You will also need to add the other files from netBuilder/postfix-conf to /etc/postfix. Clone this repository into /, and move the config files with the following
command.

    mv /trafficGen/netBuilder/postfix-conf/* /etc/postfix
    
Run the command 

    postmap login_maps virtual vmailbox 
    
to allow postfix to read the files. If you wish to change login_maps, virtual, or vmailbox, make your changes, run 

    postmap <file>
and then restart postfix with the command
    
    postfix reload 
If postfix is already shut down, use "postfix start" instead.

Below there is a list of the files in netBuilder/postfix-conf and a description of their function:
#### master.cf
This contains the services the postfix server will run.

#### main.cf
This contains the bulk of the configuration for the server. It tells postfix who to allow to send email, where to send mail, and what ip addresses can access the SMTP service. The function of all of the configuration options can be found at http://www.postfix.org/documentation.html.

#### login_maps
This contains usernames followed by an indent followed by an email address. When logged in with the username on the right, the user will be able to send mail with the address on the right. The default for this example has two users, info@example.com and sales@example.com, which are mapped to addresses of the same name.

#### virtual
This defines virtual users; in the default config found in the repo, it will cause mail intended for postmaster@example.com to be sent to root. The address on the left is the virtual address, while the user on the right is the user on the machine that will recieve the mail.

#### vmailbox
This file contains email addresses followed by the name of a directory. Email sent to those addresses will be saved in a text file /var/mail/vhosts/<the file name on the right>. Adding a '/' after the directory causes the mail to be stored in /var/mail/vhosts/<the directory on the right>/new. 
  
### Dovecot configuration
Once you have set up postfix, you will need to configure dovecot as well. First, run the following sequence of commands: 
    
    groupadd vmail -g 5000". Next, run "useradd vmail -s /bin/bash -u 5000 -g 5000 
    
    mkdir /var/mail/vhosts 
    
    mkdir /var/mail/vhosts/example.com 
    
    chown vmail /var/mail/vhosts 
    
    chown vmail /var/mail/vhosts/example.com
  Now your mail folder has been created with the proper permissions. Run the command 
  
    cp /trafficGen/netBuilder/dovecot-conf/passwd /etc/dovecot && cp /trafficGen/netBuilder/dovecot-conf/dovecot.conf /etc/dovecot && cp /trafficGen/netBuilder/dovecot-conf/10* /etc/dovecot/conf.d 
  This will copy the config files to the appropriate directories. Dovecot should not require any additional setup; simply run "service dovecot start" to start the dovecot server. The server can be connected to via the command 
  
    telnet localhost 110
    
Below is a list of the config files in netBuilder/dovecot-conf and their function. 

#### 10-auth.conf
This file tells dovecot where to find the username and password for logging into the dovecot server.

#### 10-logging.conf
This file tells dovecot where to put its log files. With the settings in this repo, dovecot will send logs to /var/log/dovecot.log and its info logs to /var/log/dovecot-info.log. Modify lines 7 and 8 to change the name or path of the log files.

#### 10-master.conf
This file is where you may add services, IE pop3 or imap servers.

#### dovecot.conf
This file tells dovecot to read the other config files, and the one in this repository creates an auth service.

#### passwd
This file contains the username and password for each account. In this repository, the passwords are stored as plaintext, but dovecot allows for them to be stored as hashes as well. the syntax is \<username>@\<domain>:{\<FORMAT>}\<password>.

### Manually send an email
To send an email, you will first need to get the base64 string containing the username and password used to log in. Echo the username and password in the format

    \000<username@example.com>\000<password>
    
and pipe into a program to convert into base 64. Make sure to use the -n and -e options on the echo command to remove the trailing newline and escape the \000's. Now type

    telnet localhost 587
from the server itself, or type 
    
    telnet <hostname.pfsense_domain.com/org/etc.> 587
to send an email remotely. The default domain should be luked.com. Type the following sequence of commands to send an email.

    ehlo there 
    AUTH PLAIN <string from earlier> 
    MAIL FROM:<sender@example.com> 
    RCPT TO:<reciever@example.com>
    data
    <Type the body of the email here>
    .
    
If you've done everything correctly, This should save the email to the text file /var/mail/vhosts/example.com/[username] or, if there is a '/' character after the right side of the vmailbox text file for that user, mail will be stored in a unique text file in the directory /var/mail/vhosts/example.com/[username]/new.

### Send email via email script
The agents/emailSender.py script from this repository will automatically send an email. By default, it will send an email from "s<the ip address of the box>@example.com" to "info@example.com". It will also attempt to connect to an email server named "studio.lrd.com" by default. To change this to send an email to a different server, or from/to a different email address, you will need to modify the script. The script will contain comments with further instructions on how to do this.

### Troubleshooting
rsyslog creates a file in /var/log called syslog, which logs interactions with the postfix server, simplifying troubleshooting. To activate rsyslog, start the rsyslog with the command 
    
    service rsyslog start
 Use 
 
     tail -n <no. lines> 
 to view the latest lines of the syslog file. This will display what went wrong after attempting and failing to access the SMTP server. Use this method to diagnose issues with postfix. After being configured, dovecot will send its logs to /var/log/dovecot.log and /var/log/dovecot-info.log. To test that dovecot is working, use 
    
    telnet localhost 110
 and type 
 
     user <username@example.com>
     pass <password>
To ensure that dovecot is properly allowing users to log in.

## Scheduler
To run the scheduler, simply type the command 
    
    python3 scheduler.py

If it prints "Call random duckduckgo query", it will tell all the boxes to query a random website. The number of these queries made will be stored on each box under "/trafficGen/agents/.queries". If the scheduler prints "Call send Email", each box will send an email to the address info@example.com. These emails will be stored in "/var/mail/vhosts/example.com/info". Finally, if the scheduler prints "Print a dummy file", each box will send a print request to the print server, named cups_pdf in the example_net.py network, and successful "prints" on the virtual printer will be stored in "/home/reciever/PDF". NOTE: this scheduler will currently only work if the example-net.py script is run while a project named "testtest" exists.

## Print Server
This is a simple print server/virtual printer setup. Like the email server, this assumes that a pfsense router with DNS is set up on the network. The default domain on the brass template will be luked.com.

### Installation
First, you will need to install the software required for this server to function. Type the following command to install all the prerequisites 
    
    apt-get update && apt-get -y install cups cups-pdf avahi-daemon git

### Configuration
To configure the cups-pdf printer, first you will need to copy netBuilder/cupsd.conf from this repo into /etc/cups. Next you will need to run the following series of commands: 

    service dubs start
    service avahi-daemon start 
    service cups start
    
 Next run the following command to create a virtual printer.
     
     lpadmin -P '/usr/share/ppd/cups-pdf/CUPS-PDF_opt.ppd' -p VPDF -E -v "cups-pdf:/" -o printer-is-shared=true
 Finally, run the following commands to create a user to store "printed" pdfs and do some final configuration: 
 
     useradd -m -s /bin/bash reciever
     cupsctl --share-printers
     cupsctl --share-printers --remote-any
     service cups restart
 Now the print server should be operational!

### Usage
To print a file, first you will need to find a pdf file to print. This repository comes with a test pdf file, downloaded from http://www.orimi.com/pdf-test.pdf. It has been renamed printThis.pdf, and is located under the 'agents' directory. To print it from the server locally, type 
    
    lp -U 'reciever' -d 'VPDF' <path-to-trafficGen-repo>/trafficGen/agents/printThis.pdf

To print it remotely, type 
    
    lp -U 'reciever' -d 'VPDF' -h '<name_of_printer_server_VM.pfsense_domain.com/org/etc.>' <path-to-traficGen-repo>/trafficGen/agents/printThis.pdf
After this has been done successfully, The command should return a response in the format

    request id is VPDF-X (1 file(s))
Where X is the number of jobs previously requested plus one.

If everythin worked correctly, a new file will appear in /home/reciever/PDF. The default domain for the pfsense template is luked.com.

## Security Onion
If you wish to visualize the data generated by this traffic, you will need to run Kibana on securityonion. First, download the securityonion template from the gns3 server. Right click the template and click 'configure template'. In the RAM: field, you will want 8-16 GB, depending on what you can spare. If you have the resources, change the vCPUs field to 2 to give the box 2 cores. Now add it to your network and start it. Run through the setup process, which the securityonion should lead you through.

### Add all dashboards through UI
Once securityonion is set up, open kibana with the shortcut on your desktop, type the username and password you created for sguil and squert (The one that required a 6+ character password). Now there should be several tabs on the left. If you are not there already, go to the management tab. There should be a small button labeld 'saved objects' on the left of the screen. Click on it, and click the import button at the top-right corner. Clone this repository. Click import in the box in the kibana UI, and select the netBuilder/export.json file in this repository. Click the blue import button. This process will take a significant amount of time. When finished this will add all dashboards and visualizations necessary to pivot from squert.

### Add dashboards through API
To add dashboards throught the API, use the add.sh script on a json file containing a dashboard object, along with associated visualizations and index patterns. A list of dashboards used for pivoting from squert can be found at github.com/Security-Onion-Solutions/securityonion-elastic.

### addall.sh
If placed in the same directory as add.sh, this script will attempt to add all json files in the current directory to kibana. Non dashboard object json files will also be attempted, but will most likely fail, which will not interupt the script. However, it is recommended that all json files in the directory with this script conatin dashboard objects and associated data, in order to avoid adding other unwanted objects.
 
