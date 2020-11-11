#!/bin/bash
if python3 getID.py node $1 $2 > /dev/null
then
    python3 getID.py project $1 > tmp.txt
    pid=$(cat tmp.txt)
    python3 getID.py node $1 $2 > tmp.txt
    nid=$(cat tmp.txt)
    rm -f tmp.txt
    #change the /data/ to whatever the path to your gns3 directory is. Change "/usa/lucasd" to some folder you have read/write permission in.
    cp "/data/gns3/projects/$pid/project-files/qemu/$nid/hda_disk.qcow2" /usa/lucasd
    cd /usa/lucasd
    mv hda_disk.qcow2 "$3.qcow2"
    mv "$3.qcow2" /data/gns3/images/QEMU
else
    echo "Something went wrong in getID.py!"
    exit 1
fi
