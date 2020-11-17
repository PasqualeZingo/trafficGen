# Files
Below there is a list of the files in this directory and a description of their function.

## master.cf
This contains the services the postfix server will run.

## main.cf
This contains the bulk of the configuration for the server. It tells postfix who to allow to send email, where to send mail, and what ip addresses can access the SMTP service. The function of all of the configuration options can be found at http://www.postfix.org/documentation.html.

## login_maps
This contains usernames followed by an indent followed by an email address. When logged in with the username on the right, the user will be able to send mail with the address on the right. The default for this example has two users, info@example.com and sales@example.com, which are mapped to addresses of the same name.

## virtual
This defines virtual users; in the default config found in the repo, it will cause mail intended for postmaster@example.com to be sent to root. The address on the left is the virtual address, while the user on the right is the user on the machine that will recieve the mail.

## vmailbox
This file contains email addresses followed by the name of a directory. Email sent to those addresses will be saved in a text file /var/mail/vhosts/<the file name on the right>. Adding a '/' after the directory causes the mail to be stored in /var/mail/vhosts/<the directory on the right>/new.
