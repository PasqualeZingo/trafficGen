# Network-attached storage server
A network-attached storage server is used essentially as a private cloud service. This network willl use the FreeNAS operating system for this purpose. The FreeNAS OS stores data in datasets, which are contained in pools. The data can be located on the server itself through a shell within /mnt/\<pool>/\<dataset>. 

## Getting the image
Within the gns3 GUI, go to file > new template. With the first option selected, click next. Under the guests dropdown menu, select the FreeNAS image. Make sure the 'Install the appliance on the main server' option is selected on the next screen. Click next. Click next on the next page. Download the files required for the latest version of the FreeNAS image. Import them, and select the version.  

## Installation
First, boot up a router. Next, start the FreeNAS image (make sure it is connected to the rest of the network through a switch!). On the first prompt, simply press enter. Select the disk ada0 with spacebar and press enter, except for the password section, in which you must first enter your password. continue pressing enter on each prompt until the computer starts installing the OS. Finally, Wait until the first prompt reappears and select the reboot option.
