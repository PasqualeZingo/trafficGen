FROM ubuntu:latest

COPY volume.sh /usr/local/bin/
COPY .query.sh /
COPY .print.sh /
COPY .email.sh /
COPY .freenas.sh /
COPY .freenasagent.sh /
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y net-tools nano ifupdown ssh iputils-ping git python3-pip firefox cups telnet nfs-common && \
    pip3 install selenium b64 numpy html5lib && \
    apt-get clean && \
    ln -s /usr/local/bin/docker-entrypoint.sh / && \
    chmod +x /usr/local/bin/volume.sh	

VOLUME /.mac_folder
VOLUME /usr/bin

ENTRYPOINT ["/usr/local/bin/volume.sh"]

