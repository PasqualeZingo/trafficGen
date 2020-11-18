# Files
The files in this directory are as follows:
## emailSender.py
A python script that will send an email from s[ip of box] to info@example.com. It contains functions that can be repurposed to send to/from arbitrary addresses.
## freeNASagent.py
Copies a random file to/from a freeNAS qemu image. Assumes files are stored in /root beforehand.
## printFile.py
Prints a test file on a print server.
## printThis.pdf
A file to be printed on the print server through printFile.py.
## userAgent.py
A script designed to make a random duckduckgo query.

# Usage
The python scripts in this directory are used by the netBuilder/traffic-gen-box to generate traffic on a network. They are called through scheduler.py in the parent directory. These scripts should only be called directly for testing purposes.
