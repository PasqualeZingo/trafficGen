# Network-attached storage server
A network-attached storage server is used essentially as a private cloud service. This network willl use the FreeNAS operating system for this purpose. The FreeNAS OS stores data in datasets, which are contained in pools. The data can be located on the server itself through a shell within /mnt/\<pool>/\<dataset>. 

## Getting the image
Within the gns3 GUI, go to file > new template. With the first option selected, click next. Under the guests dropdown menu, select the FreeNAS image. Make sure the 'Install the appliance on the main server' option is selected on the next screen. Click next. Click next on the next page. Download the files required for the latest version of the FreeNAS image. Import them, and select the version.  

## Installation
First, boot up a router. Next, start the FreeNAS image (make sure it is connected to the rest of the network through a switch!). On the first prompt, simply press enter. Select the disk ada0 with spacebar and press enter, except for the password section, in which you must first set the password to toor. continue pressing enter on each prompt until the computer starts installing the OS. Finally, Wait until the first prompt reappears and select the reboot option.

## Creating a pool and dataset
go to a traffic_gen_box container and execute the freeNAS.py script from this directory. This should automatically create a pool and a dataset. 

## Usage
To generate traffic, you should only need to interact with the image through the scheduler.py. If you do need to access the data, use the following command.

     mount FreeNAS.luked.com:/mnt/tank/MyShare /mnt
Copy whatever file you want to store to /mnt. When you are done, type 

     umount /mnt
to unmount the dataset. Any files you upload will appear in /mnt for all computers that have the dataset mounted. If you need to reconfigure the image for whatever reason, enter a browser on the network and type in the ip address of the FreeNAS box to interact with the server in a user-friendly way.
