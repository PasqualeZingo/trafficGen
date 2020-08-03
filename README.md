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

### Configuration
A clean postfix installation will have to config files within its directory at /etc/postfix. You will need to replace these files with the ones in netBuilder/postfix-conf in this repo. You will also need to add the other files from netBuilder/postfix-conf to /etc/postfix. Run "git clone https://github.com/PasqualeZingo/trafficGen" to download the files, and run "mv trafficGen/* /etc/postfix" to move the files. You may wish to remove the trafficGen directory afterwards with "rm -rf trafficGen" in the interest of saving space. Here is a list of the files in netBuilder/postfix-conf and a description of their function:
#### master.cf
This contains the services the postfix server will run.

#### main.cf
This contains the bulk of the configuration for the server. It tells postfix who to allow to send email, where to send mail, and what ip addresses can access the SMTP service. The funciton of the configuration options can be found at http://www.postfix.org/documentation.html.

#### login_maps
This contains usernames followed by an indent followed by an email address. When logged in with the username on the right, the user will be able to send mail with the address on the right. The default for this example has two users, info@example.com and sales@example.com, which are mapped to addresses of the same name.

#### virtual
This defines virtual users; in the default config found in the repo, it will


