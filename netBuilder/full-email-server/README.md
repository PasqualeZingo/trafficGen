

# Setup
See the Docker containers section in the netBuilder directory.

# Usage
This server will allow you to send email to addresses s+<ip address address from 192.168.1.100-254>. This can be done manually through the console of a device on the network, or through the agents/emailSender.py script.
## Manually send an email
To send an email, you will first need to get the base64 string containing the username and password used to log in. Echo the username and password in the format

    \000<username@example.com>\000<password>
    
and pipe into a program to convert into base 64. Make sure to use the -n and -e options on the echo command to remove the trailing newline and escape the \000's. Now type

    telnet localhost 587
from the server itself, or type 
    
    telnet <hostname.pfsense_domain.com/org/etc.> 587
to send an email remotely. The default domain for a pfsense template on brass should be luked.com. Type the following sequence of commands to send an email.

    ehlo there 
    AUTH PLAIN <string from earlier> 
    MAIL FROM:<sender@example.com> 
    RCPT TO:<reciever@example.com>
    data
    <Type the body of the email here>
    .
    
If you've done everything correctly, This should save the email to the text file /var/mail/vhosts/example.com/[username] or, if there is a '/' character after the right side of the vmailbox text file for that user, mail will be stored in a unique text file in the directory /var/mail/vhosts/example.com/[username]/new.

## Send email via email script
The agents/emailSender.py script from this repository will automatically send an email. By default, it will send an email from "s<the ip address of the box>@example.com" to "info@example.com". It will also attempt to connect to an email server named "studio.lrd.com" by default. To change this to send an email to a different server, or from/to a different email address, you will need to modify the script. The script will contain comments with further instructions on how to do this.

# Troubleshooting
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

# Files
Below is a list of files in this directory.

## dovecot-conf
A directory containing files that configure dovecot.

## postfix-conf
A directory containing files that configure postfix.

## Dockerfile
A dockerfile for building an image to host the email server.

## adds.py
A script to add users to the email server.

## server.sh
An entrypoint script, which is run on the startup of a container. Creates the email server through the method outlined below. 

# Creating an Email server from a test-client (This is going to be removed soon! Only here to remind me so I can document server.sh!)
This is perhaps the most difficult of the three servers to set up and configure. This server will allow the userAgent to send emails via telnet to predefined users after authentication. This tutorial assumes you already have a pfsense router with DNS configured. The template on brass will have the default domain luked.com, however, if the email server is named "studio", it will recieve a static ip of 192.168.1.1 and a unique domain of lrd.com. Keep this in mind when telneting into the server.

## Installation
The first step to setting up the server is to install the software that the server will use to relay the mail, along with other basic utilities. To do this, run the following command:

    apt-get update && apt-get install -y rsyslog telnet postfix dovecot-common dovecot-imapd dovecot-pop3d git
The postfix and dovecot packages are used for sending mail and authentication, respectively. Rsyslog simplifies troubleshooting postfix. Telnet is used to interact with the Simple Mail Transfer Protocol (SMTP for short) server for testing purposes.

## Postfix configuration
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
  
## Dovecot configuration
Once you have set up postfix, you will need to configure dovecot as well. First, run the following sequence of commands: 
    
    groupadd vmail -g 5000
    
    useradd vmail -s /bin/bash -u 5000 -g 5000 
    
    mkdir /var/mail/vhosts 
    
    mkdir /var/mail/vhosts/example.com 
    
    chown vmail /var/mail/vhosts 
    
    chown vmail /var/mail/vhosts/example.com
  Now your mail folder has been created with the proper permissions. Run the command 
  
    cp /trafficGen/netBuilder/dovecot-conf/passwd /etc/dovecot && cp /trafficGen/netBuilder/dovecot-conf/dovecot.conf /etc/dovecot && cp /trafficGen/netBuilder/dovecot-conf/10* /etc/dovecot/conf.d 
  This will copy the config files to the appropriate directories. Dovecot should not require any additional setup; simply run "service dovecot start" to start the dovecot server. The server can be connected to via the command 
  
    telnet localhost 110
