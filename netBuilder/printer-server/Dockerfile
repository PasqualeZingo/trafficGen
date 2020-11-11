FROM ubuntu:latest

COPY server.sh /usr/local/bin/

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y rsyslog telnet net-tools nano ifupdown ssh iputils-ping cups cups-pdf avahi-daemon && \
    apt-get clean && \
    ln -s /usr/local/bin/docker-entrypoint.sh / && \
    chmod +x /usr/local/bin/server.sh	

VOLUME /.mac_folder
COPY cupsd.conf /etc/cups

ENTRYPOINT ["/usr/local/bin/server.sh"]

