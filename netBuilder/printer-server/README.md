# Print Server
This is a simple print server/virtual printer setup. Like the email server, this assumes that a pfsense router with DNS is set up on the network. The default domain on the brass template will be luked.com.

## Installation
First, you will need to install the software required for this server to function. Type the following command to install all the prerequisites 
    
    apt-get update && apt-get -y install cups cups-pdf avahi-daemon git

## Configuration
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

## Usage
To print a file, first you will need to find a pdf file to print. This repository comes with a test pdf file, downloaded from http://www.orimi.com/pdf-test.pdf. It has been renamed printThis.pdf, and is located under the 'agents' directory. To print it from the server locally, type 
    
    lp -U 'reciever' -d 'VPDF' <path-to-trafficGen-repo>/trafficGen/agents/printThis.pdf

To print it remotely, type 
    
    lp -U 'reciever' -d 'VPDF' -h '<name_of_printer_server_VM.pfsense_domain.com/org/etc.>' <path-to-traficGen-repo>/trafficGen/agents/printThis.pdf
After this has been done successfully, The command should return a response in the format

    request id is VPDF-X (1 file(s))
Where X is the number of jobs previously requested plus one.

If everything worked correctly, a new file will appear in /home/reciever/PDF. The default domain for the pfsense template is luked.com.
