FROM ubuntu:latest

COPY server.sh /usr/local/bin/

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y rsyslog telnet net-tools nano postfix ifupdown ssh iputils-ping s-nail git dovecot-common dovecot-imapd dovecot-pop3d && \
    apt-get clean && \
    ln -s /usr/local/bin/docker-entrypoint.sh / && \
    chmod +x /usr/local/bin/server.sh	

VOLUME /.mac_folder
COPY postfix-conf/* /etc/postfix/
COPY dovecot-conf/10*.conf /etc/dovecot/conf.d/
COPY dovecot-conf/dovecot.conf /etc/dovecot/
COPY dovecot-conf/passwd /etc/dovecot/
COPY adds.py /etc/postfix
ENTRYPOINT ["/usr/local/bin/server.sh"]

