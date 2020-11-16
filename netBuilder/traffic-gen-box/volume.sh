#!/bin/bash

echo "auto eth0" > /etc/network/interfaces
echo "iface eth0 inet dhcp" >> /etc/network/interfaces
echo "nameserver 192.168.1.1" > /etc/resolv.conf
echo  "Include /etc/ssh/sshd_config.d/*.conf" > /etc/ssh/sshd_config
echo  "Port 22" >> /etc/ssh/sshd_config
echo "Port 2222" >> /etc/ssh/sshd_config

if [ -f /.mac_folder/this_is_the_mac ]
then
mac=$(cat /.mac_folder/this_is_the_mac)
ifconfig eth0 down hw ether $mac && ifconfig eth0 up
service networking restart
else
mac=$(ifconfig | grep -o "ether.* " | cut -d ' ' -f 2)
echo "the MAC address of this box is $mac"
echo "$mac" > /.mac_folder/this_is_the_mac
fi

dhclient -v

if [ -f /usr/bin/geckodriver ]
then
echo "geckodriver already present. Skipping installation."
else
echo "installing geckodriver..."
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xvzf /geckodriver*
chmod 777 /geckodriver
rm -r geckodriver-v0.26.0-linux64.tar.gz
mv geckodriver /usr/bin
fi

echo "alias lpr=\"lp -U 'reciever' -h 'cups_pdf.luked.com' -d 'VPDF'\"" >> /root/.bashrc

until [ -d /trafficGen ]
do
    rm -rf /trafficGen
    git clone https://github.com/PasqualeZingo/trafficGen
done

touch /root/file{1..10}

service rpcbind start
service nfs-common start
service ssh start
ifup eth0
bash
	
