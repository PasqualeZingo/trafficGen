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
In order to generate traffic, you will need to have a virtual network with servers that the useragent can interact with. Currently, these consist of a print server, an email server, and a network-attached storage server.

## Email server
This is perhaps the most difficult of the three servers to set up and configure. This server will allow the userAgent to send emails via telnet to predefined users after authentication.

### Installation
The first step to setting up the server is to install the software that the server will use to relay the mail, along with other basic utilities. To do this, run the following command:
"apt-get update && apt-get install -y rsyslog telnet postfix dovecot-common dovecot-imapd dovecot-pop3d git"
The postfix and dovecot packages are used for sending mail and authentication, respectively. rsyslog creates a file in /var/log called syslog, which logs interactions with the postfix server, simplifying troubleshooting. To activate rsyslog, start the rsyslog with the command 'service rsyslog start'. Use the tail -n (no. lines) to view the latest lines of the syslog file. Telnet is used to interact with the SMTP server for testing purposes.

### Postfix configuration
A clean postfix installation will have to config files within its directory at /etc/postfix. You will need to replace these files with the ones in netBuilder/postfix-conf in this repo. You will also need to add the other files from netBuilder/postfix-conf to /etc/postfix. Run "git clone https://github.com/PasqualeZingo/trafficGen" to download the files, and run "mv /trafficGen/netBuilder/postfix-conf/* /etc/postfix" to move the files. Run the command "postmap login_maps virtual vmailbox" to allow postfix to read the files. If you wish to change login_maps, virtual, or vmailbox, make your changes, run "postmap <file>", and then restart postfix with the command "postfix reload" (assuming postfix is running when you make the changes. If it is shut down, use "postfix start" instead.) Below there is a list of the files in netBuilder/postfix-conf and a description of their function:
#### master.cf
This contains the services the postfix server will run.

#### main.cf
This contains the bulk of the configuration for the server. It tells postfix who to allow to send email, where to send mail, and what ip addresses can access the SMTP service. The funciton of the configuration options can be found at http://www.postfix.org/documentation.html.

#### login_maps
This contains usernames followed by an indent followed by an email address. When logged in with the username on the right, the user will be able to send mail with the address on the right. The default for this example has two users, info@example.com and sales@example.com, which are mapped to addresses of the same name.

#### virtual
This defines virtual users; in the default config found in the repo, it will cause mail intended for postmaster@example.com to be sent to root. The address on the left is the virtual address, while the user on the right is the user on the machine that will recieve the mail.

#### vmailbox
This file contains email addresses followed by the name of a directory. Email sent to those addresses will be saved in a text file /var/mail/vhosts/<the file name on the right>. Adding a '/' after the directory causes the mail to be stored in /var/mail/vhosts/<the directory on the right>/new. 
  
### Dovecot configuration
Once you have set up postfix, you will need to configure dovecot as well. First, run "groupadd vmail -g 5000". Next, run "useradd vmail -s /bin/bash -u 5000 -g 5000". Next, run "mkdir /var/mail/vhosts" and "mkdir /var/mail/vhosts/example.com". Finally, run "chown vmail /var/mail/vhosts" and "chown vmail /var/mail/vhosts/example.com". Now your mail folder has been created with the proper permissions. Run the command "cp /trafficGen/netBuilder/dovecot-conf/passwd /etc/dovecot && cp /trafficGen/netBuilder/dovecot-conf/dovecot.conf /etc/dovecot && cp /trafficGen/netBuilder/dovecot-conf/10* /etc/dovecot/conf.d". This will copy the config files to the appropriate directories. Dovecot should not require any additional setup; simply run "service dovecot start" to start the dovecot server. The server can be connected to via the command "telnet localhost 110". Below is a list of the config files in netBuilder/dovecot-conf and their function. 

#### 10-auth.conf
This file tells dovecot where to find the username and password for logging into the dovecot server.

#### 10-logging.conf
This file tells dovecot where to put its log files. With the settings in this repo, dovecot will send logs to /var/log/dovecot.log and its info logs to /var/log/dovecot-info.log. Modify lines 7 and 8 to change the name or path of the log files.

#### 10-master.conf
This file is where you may add services, IE pop3 or imap servers.

#### dovecot.conf
This file tells dovecot to read the other config files, and the one in this repository creates an auth service.

#### passwd
This file contains the username and password for each account. In this repository, the passwords are stored as plaintext, but dovecot allows for them to be stored as hashes as well. the syntax is <username>@<domain>:{<FORMAT>}<password>.



