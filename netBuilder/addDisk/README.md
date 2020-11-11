# Usage
type

    ./addDisk.sh <project_name> <node_name> <disk_name>
to copy the disk of the chosen node from the chosen project into your gns3/images/QEMU file and rename it to disk_name.

# Troubleshooting
You may need to modify the getdisk.sh script to work on your environment. In the script there are instructions on what lines to change. You should not need to modify getID.py. If the script gives the error message "something went wrong in getID.py!", make sure you supplied the arguments in the correct order, and check that they are spelled correctly.
