#!/bin/bash
echo "nameserver 192.168.1.1" > /etc/resolv.conf
echo "92:b9:ae:84:60:00" > /.mac_folder/mac
mac=$(cat /.mac_folder/mac)
ifconfig eth0 down hw ether $mac && ifconfig eth0 up

dhclient

groupadd -g 5000 vmail
useradd -g 5000 -u 5000 -m -s /bin/bash vmail

postmap /etc/postfix/virtual

chown vmail /var/mail
mkdir /var/mail/vhosts
mkdir /var/mail/vhosts/example.com
chown vmail /var/mail/vhosts
chown vmail /var/mail/vhosts/example.com

cd /etc/postfix

for x in $(seq 100 254)
do
	echo "s192.168.1.$x@example.com" >> addresses
done

python3 adds.py

mv addresses /etc/dovecot
mv adds.py /etc/dovecot
cd /etc/dovecot
python3 adds.py

echo  "Include /etc/ssh/sshd_config.d/*.conf" > /etc/ssh/sshd_config
echo  "Port 22" >> /etc/ssh/sshd_config
echo "Port 2222" >> /etc/ssh/sshd_config

postmap /etc/postfix/vmailbox
postmap /etc/postfix/login_maps

rm /etc/dovecot/addresses
rm /etc/dovecot/adds.py
rm /etc/postfix/passwd

echo "#!/bin/bash" > /usr/local/bin/getAuth
echo -n "echo -ne \"\000\$1@example.com\000password\" | openssl base64" >> /usr/local/bin/getAuth
chmod +x /usr/local/bin/getAuth

postfix start
service dovecot start
service rsyslog start
cd /var/mail/vhosts/example.com
bash
