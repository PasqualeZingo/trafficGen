# Executing commands on containers
  The files in this directory are all used to execute commands on active docker containers. To view the currently active containers, use the command 'docker container ls'.
Take note that the names of the containers stored by docker are distinct from the hostnames of the machines themselves.

## run.sh
  This script executes a command specified by the second argument within the container specified by the first. See the comments within the script for more detail.

## runall.sh
  This script runs the command specified by the first argument within all active containers with a _hostname_ beginning with the string "traffic_gen_box". Remember that the hostname is distinct from the name of the container.

## gethost.sh
  This script is used by runall.sh to view the hostname of each container. It is not intended to be executed by a user directly.
