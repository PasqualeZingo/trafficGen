#!/bin/bash
#If the node can be found:
if python3 getID.py node $1 $2 > /dev/null
then
    #Store the id of the project in tmp.txt and read it.
    python3 getID.py project $1 > tmp.txt
    pid=$(cat tmp.txt)
    #Store the id of the node in tmp.txt and read it.
    python3 getID.py node $1 $2 > tmp.txt
    nid=$(cat tmp.txt)
    #Get rid of tmp.txt.
    rm -f tmp.txt
    #change the /data/ to whatever the path to your gns3 directory is. Change "/usa/lucasd" to some folder you have read/write permission in.
    cp "/data/gns3/projects/$pid/project-files/qemu/$nid/hda_disk.qcow2" /usa/lucasd
    #change /usa/lucasd to some directory where you have read-write permission.
    cd /usa/lucasd
    mv hda_disk.qcow2 "$3.qcow2"
    #Again, change /data/ to whereever gns3 is stored in your environment.
    mv "$3.qcow2" /data/gns3/images/QEMU
else
    echo "Something went wrong in getID.py!"
    exit 1
fi
