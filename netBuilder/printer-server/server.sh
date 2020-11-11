#!/bin/bash
echo "nameserver 192.168.1.1" > /etc/resolv.conf
echo "92:b9:ae:84:60:01" > /.mac_folder/mac
mac=$(cat /.mac_folder/mac)
ifconfig eth0 down hw ether $mac && ifconfig eth0 up

dhclient

echo  "Include /etc/ssh/sshd_config.d/*.conf" > /etc/ssh/sshd_config
echo  "Port 22" >> /etc/ssh/sshd_config
echo "Port 2222" >> /etc/ssh/sshd_config

service dbus start
service avahi-daemon start
service cups start
service rsyslog start

lpadmin -P '/usr/share/ppd/cups-pdf/CUPS-PDF_opt.ppd' -p VPDF -E -v "cups-pdf:/" -o printer-is-shared=true

useradd -m -s /bin/bash reciever
cupsctl --share-printers
cupsctl --share-printers --remote-any
service cups restart
cd /home/reciever
bash
