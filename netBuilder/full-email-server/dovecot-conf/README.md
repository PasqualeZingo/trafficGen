# Files
Below is a list of files in this directory and their purpose. If you wish to reconfigure the email server image, you will need to re-build the image.

## 10-auth.conf
This file tells dovecot where to find the username and password for logging into the dovecot server.

## 10-logging.conf
This file tells dovecot where to put its log files. With the settings in this repo, dovecot will send logs to /var/log/dovecot.log and its info logs to /var/log/dovecot-info.log. Modify lines 7 and 8 to change the name or path of the log files.

## 10-master.conf
This file is where you may add services, IE pop3 or imap servers.

## dovecot.conf
This file tells dovecot to read the other config files, and the one in this repository creates an auth service.

## passwd
This file contains the username and password for each account. In this repository, the passwords are stored as plaintext, but dovecot allows for them to be stored as hashes as well. the syntax is \<username>@\<domain>:{\<FORMAT>}\<password>.
