#!/bin/bash
#set the DNS server to the IP address 192.168.1.1
echo "nameserver 192.168.1.1" > /etc/resolv.conf
#Set the MAC address to this value
echo "92:b9:ae:84:60:01" > /.mac_folder/mac
mac=$(cat /.mac_folder/mac)
#Turn the network connection off and on
ifconfig eth0 down hw ether $mac && ifconfig eth0 up

#Connect to the DHCP server
dhclient

#Configure ssh
echo  "Include /etc/ssh/sshd_config.d/*.conf" > /etc/ssh/sshd_config
echo  "Port 22" >> /etc/ssh/sshd_config
echo "Port 2222" >> /etc/ssh/sshd_config

#Prepare the services required to run the print server
service dbus start
service avahi-daemon start
service cups start
service rsyslog start

#Create the printer VPDF
lpadmin -P '/usr/share/ppd/cups-pdf/CUPS-PDF_opt.ppd' -p VPDF -E -v "cups-pdf:/" -o printer-is-shared=true

#Add a user to recieve print requests
useradd -m -s /bin/bash reciever
#Make sure cups accepts requests from other machines.
cupsctl --share-printers
cupsctl --share-printers --remote-any
#make the updates take effect
service cups restart
#Set the pwd to reciever's home directory. This is where the server will store the output of the virtual printer, in a directory named PDF which will be created when a print request is processed.
cd /home/reciever
bash
