# Network-attached storage server
A network-attached storage server is used essentially as a private cloud service. This network willl use the FreeNAS operating system for this purpose. The FreeNAS OS stores data in datasets, which are contained in pools. The data can be located on the server itself through a shell within /mnt/\<pool>/\<dataset>. 

## Getting the image
Within the gns3 GUI, go to file > new template. With the first option selected, click next. Under the guests dropdown menu, select the FreeNAS image. Make sure the 'Install the appliance on the main server' option is selected on the next screen. Click next. Click next on the next page. Download the files required for the latest version of the FreeNAS image. Import them, and select the version.  

## Installation
On the first prompt, simply press enter.
