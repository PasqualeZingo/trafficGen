# Files
This directory contains the following files.
## agents
A directory containing scripts designed to generate traffic on a virtual network. The scripts are documented in more detail within the code itself.
## netBuilder
A directory containing the necessary files and instructions to build a virtual network on gns3. More information in the README within the directory.
## .gitignore
This file tells git to ignore some files.
# runall.py
A python module containing functions that allow other scripts to run executable scripts in docker containers. More details in the documentation within the script itself.
## scheduler.py
A script that will periodically use the runall.py script to run a random script from agents on all the docker images named traffic_gen_box to generate traffic.

# trafficGen
This is a mono repo containing everything needed to operate and develop on the virtualized network within brass.
## Prereqs
### VMWare Workstation
The UD College of Engineering provides a number of different softwares through UDeploy. Our development VM runs on VMware Workstation which can be downloaded from [UDeploy here](https://udeploy.udel.edu/software/vmware-for-university-of-delaware/)


### UD VPN
In order to connect to brass, you need to be connected to the UD network. [The UD AnyConnect VPN](https://udeploy.udel.edu/software/anyconnect-vpn/) can be found here. If you haven't already, the UD VPN also requires a second password, which is generated through google authenticator. You can set that up by following the instructions layed out on this [webpage](https://services.udel.edu/TDClient/32/Portal/KB/ArticleDet?ID=4)


### IDS-ML VM
Our VM image is hosted on google drive which can be downloaded here. #TODO insert vm image link

## Parts of this repo
* GNS3
* UserAgent
* ML 

# Scheduler usage
To run the scheduler, simply type the command 
    
    python3 scheduler.py

If it prints "Call random duckduckgo query", it will tell all the boxes to query a random website. The number of these queries made will be stored on each box under "/trafficGen/agents/.queries". If the scheduler prints "Call send Email", each box will send an email to the address info@example.com. These emails will be stored in "/var/mail/vhosts/example.com/info". Finally, if the scheduler prints "Print a dummy file", each box will send a print request to the print server, named cups_pdf in the example_net.py network, and successful "prints" on the virtual printer will be stored in "/home/reciever/PDF". NOTE: this scheduler will currently only work if the example-net.py script is run while a project named "testtest" exists.

