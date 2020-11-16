FROM ubuntu:latest

COPY internet.sh /usr/local/bin/

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y nfs-common net-tools nano ifupdown ssh iputils-ping cups ssmtp telnet cups avahi-daemon && \
    apt-get clean && \
    ln -s /usr/local/bin/docker-entrypoint.sh / && \
    chmod +x /usr/local/bin/internet.sh

ENTRYPOINT ["/usr/local/bin/internet.sh"]

