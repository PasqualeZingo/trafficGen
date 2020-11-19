# Adding QEMU image templates in gns3
Most of the machines on the virtual network are run on either QEMU or docker. To add a QEMU machine to a gns3 network, either through the API or the GUI, you will need to add a template for it to gns3. To add a template, go to file > new template. Click next, then select the appropriate machine. Download and import the required files for the version you want (most likely the lastest version). With the version selected, click next again. Finally, click finish. You will now be able to access the image through the button on the left corresponding to the category of the machine. 

# Network setup
In order to generate traffic, you will need to have a virtual network with servers that the useragent can interact with. Currently, these consist of a print server, an email server, and a network attached storage server. This tutorial explains how to create these servers on a gns3 network. You will need to have docker installed on the machine running the network. The first device you will want working is a router. It is strongly recommended that you use the pfsense device as a router. The template is located under firewalls when creating a new template.

## Pfsense
Pfsense is an open-source firewall software that can be used as a router.
### Installation
Refer to Adding QEMU image templates in gns3 to see how to create a template for pfsense. As of the current version of gns3, the versions of pfsense it has listed are out of date. If this is still the case, you will need to move the pfsense iso and the empty 100G disk image to your gns3/images/QEMU directory, add a new qemu image, and right click on it to configure the template. Under general settings, give the template 2048 MB of ram and 1 vcpu. Under the HDD tab, enter empty100G.qcow2 in the first text box. Under CD/DVD, type the name of your pfsense iso in the text box. Click apply. This should give you a template that will run as a pfsense router. Now you will need to drag and drop the template into your network. You should also drop a NAT node into the network and an ethernet hub. click on the button with the image of a cable, click on the router, select em0, and connect it to the NAT cloud. Next, connect em1 to the ethernet hub. Now right click the node to start it and open a console. From there, you should be able to step through the installation process by pressing enter on the first option for each popup. 

## Configuration
The first step of configuring the router is to make sure the interfaces are assigned properly. In the pfsense console after booting, select option 1. Do not set up vlan. set the WAN interface to em0 (The one connected to the NAT node) and the LAN interface to em1 (the one connected to the hub). If it asks you to set optional interfaces, simply set them to each remaining interface.

## webconfigurator
To configure pfsense, open a browser on the network connected to it, and type its ip address into the search bar. By default, this ip address should be 192.168.1.1. The username is admin, and the password is pfsense. There will be a warning at the top informing you that the router still has the default username and password; this can be safely ignored on an isolated virtual network. 

## Domain
Click the three lines at the top right to open the menu. Go to system > General setup. The second field should be domain. Change this to luked.com.

### DNS
Next, go to services > DNS resolver. The options you will need to be concerned with are listed below.

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

# Docker containers
This directory contains the directories full-email-server and printer-server. These each contain a Dockerfile, an entrypoint script, and a README file describing how the entrypoint script converts a blank linux container to the required server, and how to use the server once it is finished. The documentation also describes how to reconfigure the servers. Note that docker containers are not persistent; rebooting them will delete anything you have done to them!
## Creating the server images
To create docker images from these directories, cd into them and run the command

    docker build . -t <name_of_image>
Use the following command to verify that the image was added:

    docker image ls
## Adding the images to gns3
To add these images as templates in gns3, click on the "browse end devices" button on the bar on the right (the button with the picture of a desktop monitor). Next, in the popup window, click on the bottom border of the popup, where it says "New template". This will create another popup window. In this window, click the bubble titled "Manually create a new template". This will create another window, which will have categories of options on the left. Select docker at the bottom left, and go to docker containers. In the panel this brings up, click the 'new' button. This will bring up yet another window, with a dropdown menu. Select the image of the name you selected earlier in the dropdown menu. Click next. Choose a name for the gns3 template (this does not need to be the same as the image name). Click next until the window closes. If you press the browse end devices button again, you should see the template you just created, and you can add it to your network by dragging and dropping it in. The email server and printer server may not function properly if they are not connected to a DNS-enabled router.


# Security Onion
If you wish to visualize the data generated by this traffic, you will need to run Kibana on securityonion. First, download the securityonion template from the gns3 server. Right click the template and click 'configure template'. In the RAM: field, you will want 8-16 GB, depending on what you can spare. If you have the resources, change the vCPUs field to 2 to give the box 2 cores. Now add it to your network and start it. Run through the setup process, which the securityonion should lead you through.

### Add all dashboards through UI
Once securityonion is set up, open kibana with the shortcut on your desktop, type the username and password you created for sguil and squert during setup (The one that required a 6+ character password). Now there should be several tabs on the left. If you are not there already, go to the management tab. There should be a small button labeld 'saved objects' on the left of the screen. Click on it, and click the import button at the top-right corner. Clone this repository. Click import in the box in the kibana UI, and select the netBuilder/export.json file in this repository. Click the blue import button. This process will take a significant amount of time. When finished this will add all dashboards and visualizations necessary to pivot from squert.

### Add dashboards through API
To add dashboards throught the API, use the add.sh script on a json file containing a dashboard object, along with associated visualizations and index patterns. A list of dashboards used for pivoting from squert can be found at github.com/Security-Onion-Solutions/securityonion-elastic.

### addall.sh
If placed in the same directory as add.sh, this script will attempt to add all json files in the current directory to kibana. Non dashboard object json files will also be attempted, but will most likely fail, which will not interupt the script. However, it is recommended that all json files in the directory with this script conatin dashboard objects and associated data, in order to avoid adding other unwanted objects.
 
# Copying configurations
re-configuring the securityonion, FreeNAS, and pfsense virtual machines every time you need a new network would be time-consuming. Instead, use the addDisk/addDisk.sh script save the disk of your configured device. Then, configure the templates by right-clicking them in the appropriate menu in the gns3 GUI, go to HDD and change the top disk image to whatever you saved the disk as (the third argument to addDisk.sh).
## FreeNAS
note that this image will have two disks, but its directory will contain only one disk image. Following the steps above will still allow you to skip the installation process, however, it will not save pools or datasets you create. Thus, you will need to use the script in freeNAS to create new ones each time. See the documetation in freeNAS to learn more.

# Directories
This is a description of the contents of each subdirectory of netBuilder. Each one will contain further details.
## add-to-kibana
This contains two scripts for adding dashboards to kibana through the API. This allows you to see the traffic on the network on the Security onion VM (explained below).

## addDisk
This contains scripts used to find a node in a project and copy its disk to save the setup on the machine. This will only work for QEMU images.

## freeNAS
This contains a script used to get a FreeNAS machine ready for use.

## full-email-server
This contains the dockerfile, entrypoint script, and config files required to create a docker image that will host a functional postfix-dovecot email server, which will require authentication to enter.

## printer-server
This contains the dockerfile, entrypoint script, and config file necessary to run a cups print server and a cups-pdf virtual printer.

## test-client
This contains the dockerfile and entrypoint script required to set up a client with the software necessary to send emails, print requests, or to share files over the network-attached storage server. Used for debugging, not generating traffic.

## traffic-gen-box
This contains the dockerfile and entrypoint script for a docker image designed to create traffic on the network. The image created from this directory (see docker containers section) must be named traffic_gen_box for the scheduler.py script to function.

## export.json
A set of dashboards that, if uploaded to kibana through the api, will track the network traffic.
