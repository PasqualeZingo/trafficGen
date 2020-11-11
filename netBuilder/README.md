# Network setup
In order to generate traffic, you will need to have a virtual network with servers that the useragent can interact with. Currently, these consist of a print server, an email server, and a network attached storage server. This tutorial explains how to create these servers on a gns3 network. You will need to have docker installed on the machine running the network. 

## Pfsense config
To configure pfsense, open a browser on the network connected to it, and type its ip address into the search bar. For the default template on brass, that ip is 192.168.1.1.
The username is admin, and the password is pfsense. There will be a warning at the top informing you that the router still has the default username and password; this can be safely ignored on an isolated virtual network. The default domain for the router is luked.com. 

### DNS
To configure the DNS resolver, click the three lines at the top right corner. In the drop-down menu that appears, click services > DNS resolver. The options you will need to be concerned with are listed below.

#### Enable
Whether DNS is allowed on the server. This _must_ be on.

#### Network Interfaces
Which interfaces respond to DNS requests. Set this to all. 

#### Outgoing Network Interfaces
Which interface is used to find other DNS servers. Set to All or WAN.

#### DHCP Registration
Clients tell the server their hostname when requesting an IP address from the DHCP server. This will allow you to ping anything on the network by typing the command

    ping <hostname>.<domain>

#### Static DHCP
Allows mapping clients with a specific name to a specific IP address. Something similar can be achieved through the DHCP Static Mappings for this Interface option under Services > DHCP server, though this will require knowledge of the client's MAC address.

## Print Server
This is a simple print server/virtual printer setup. Like the email server, this assumes that a pfsense router with DNS is set up on the network. The default domain on the brass template will be luked.com.

### Installation
First, you will need to install the software required for this server to function. Type the following command to install all the prerequisites 
    
    apt-get update && apt-get -y install cups cups-pdf avahi-daemon git

### Configuration
To configure the cups-pdf printer, first you will need to copy netBuilder/cupsd.conf from this repo into /etc/cups. Next you will need to run the following series of commands: 

    service dubs start
    service avahi-daemon start 
    service cups start
    
 Next run the following command to create a virtual printer.
     
     lpadmin -P '/usr/share/ppd/cups-pdf/CUPS-PDF_opt.ppd' -p VPDF -E -v "cups-pdf:/" -o printer-is-shared=true
 Finally, run the following commands to create a user to store "printed" pdfs and do some final configuration: 
 
     useradd -m -s /bin/bash reciever
     cupsctl --share-printers
     cupsctl --share-printers --remote-any
     service cups restart
 Now the print server should be operational!

### Usage
To print a file, first you will need to find a pdf file to print. This repository comes with a test pdf file, downloaded from http://www.orimi.com/pdf-test.pdf. It has been renamed printThis.pdf, and is located under the 'agents' directory. To print it from the server locally, type 
    
    lp -U 'reciever' -d 'VPDF' <path-to-trafficGen-repo>/trafficGen/agents/printThis.pdf

To print it remotely, type 
    
    lp -U 'reciever' -d 'VPDF' -h '<name_of_printer_server_VM.pfsense_domain.com/org/etc.>' <path-to-traficGen-repo>/trafficGen/agents/printThis.pdf
After this has been done successfully, The command should return a response in the format

    request id is VPDF-X (1 file(s))
Where X is the number of jobs previously requested plus one.

If everything worked correctly, a new file will appear in /home/reciever/PDF. The default domain for the pfsense template is luked.com.


## Network-attached storage server
A network-attached storage server is used essentially as a private cloud service. This network willl use the FreeNAS operating system for this purpose. The FreeNAS OS stores data in datasets, which are contained in pools. The data can be located on the server itself through a shell within /mnt/\<pool>/\<dataset>. 

### Setup 
  In order to share data, the server will need to be told to set up a share using the service appropriate for the Operating Systems used by other machines on the network. The freeNAS.py script uses nfs, which is used for UNIX operating systems such as linux. The FreeNAS template on brass already has version 11.3-U4 of the FreeNAS OS installed. It also has a pool, dataset, and share, but these were not saved properly and will not function. As such, you will need to use the netBuilder/freeNAS.py script to set up a working area to store data. To run the script, type the following command.
  
    python3 <location of repo>/trafficGen/netBuilder/freeNAS.py
  If it does not work, check to make sure that the domain of the router is luked.com. If it is something else, modify the script accordingly. This script should function from any computer on a network with the FreeNAS VM, as long as the root password has not be modified. Once the script has been run successfully, it should display several json objects, representing the objects created by the script. The comments and doc strings within freeNAS.py will give a more detailed run down of how the objects are being created. 

### Usage
  Once the freeNAS.py script has been executed, any machine with the nfs-common package installed should be capable of interacting with the new share. Type the following commands to access the share:
  
    service nfs-common start
    mount FreeNAS.luked.com:/mnt/tank/MyShare /mnt
  After running these commands, any files added to or deleted from the directory /mnt will be added to the appropriate dataset on the FreeNAS server. Any other machines with the dataset mounted will see the changes occur in real time. To unmount the dataset, in order to modify it or for some other reason, type the following command. Note that this will not work if the current working directory is /mnt.
  
    umount /mnt

# Security Onion
If you wish to visualize the data generated by this traffic, you will need to run Kibana on securityonion. First, download the securityonion template from the gns3 server. Right click the template and click 'configure template'. In the RAM: field, you will want 8-16 GB, depending on what you can spare. If you have the resources, change the vCPUs field to 2 to give the box 2 cores. Now add it to your network and start it. Run through the setup process, which the securityonion should lead you through.

### Add all dashboards through UI
Once securityonion is set up, open kibana with the shortcut on your desktop, type the username and password you created for sguil and squert during setup (The one that required a 6+ character password). Now there should be several tabs on the left. If you are not there already, go to the management tab. There should be a small button labeld 'saved objects' on the left of the screen. Click on it, and click the import button at the top-right corner. Clone this repository. Click import in the box in the kibana UI, and select the netBuilder/export.json file in this repository. Click the blue import button. This process will take a significant amount of time. When finished this will add all dashboards and visualizations necessary to pivot from squert.

### Add dashboards through API
To add dashboards throught the API, use the add.sh script on a json file containing a dashboard object, along with associated visualizations and index patterns. A list of dashboards used for pivoting from squert can be found at github.com/Security-Onion-Solutions/securityonion-elastic.

### addall.sh
If placed in the same directory as add.sh, this script will attempt to add all json files in the current directory to kibana. Non dashboard object json files will also be attempted, but will most likely fail, which will not interupt the script. However, it is recommended that all json files in the directory with this script conatin dashboard objects and associated data, in order to avoid adding other unwanted objects.
 
