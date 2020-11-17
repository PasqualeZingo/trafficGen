# Files
Below is a list of files in this directory. The hidden files are there to trigger other scripts, since commands given by scheduler.py tell the target to execute a file, not a command. These will be labeled with the file they are designed to trigger.
## .email.sh (Hidden)
agents/emailSender.py

## .freenas.sh (Hidden)
netBuilder/FreeNAS/freeNAS.py

## .freenasagent.sh (Hidden)
agents/freeNASagent.py

## .print.sh (Hidden)
agents/printFile.py

## .query.sh (Hidden)
agents/userAgent.py

## Dockerfile
A file used to build this docker image

## printThis.pdf
A pdf file for the agents/printFile.py script to print.

## volume.sh
The entrypoint script that is run whenever a container of this image is started.

# Usage
see the docker container section at the bottom of netbuilder/README.md.
