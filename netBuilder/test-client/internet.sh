#!/bin/bash

echo "auto eth0" > /etc/network/interfaces
echo "iface eth0 inet dhcp" >> /etc/network/interfaces
echo "nameserver 192.168.1.1" > /etc/resolv.conf
echo  "Include /etc/ssh/sshd_config.d/*.conf" > /etc/ssh/sshd_config
echo  "Port 22" >> /etc/ssh/sshd_config
echo "Port 2222" >> /etc/ssh/sshd_config
echo "alias lpr=\"lp -h 'printer.luked.com' -d 'VPDF' -U reciever\"" >> /root/.bashrc

service rpcbind start
service nfs-common start
ifup eth0
service ssh start
bash
