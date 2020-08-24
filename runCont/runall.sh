#!/bin/bash

#Gets the names of all active docker containers.
echo "$(docker container ls | cut -d ' ' -f 1)" > contls

#Gets the number of lines in contls and stores it in the variable len.
len=$(wc -l contls | cut -d ' ' -f 1)

#subtracts one from len, making it the number of active containers.
let "len=len-1"

#For each container currently active...
for ID in $(tail contls -n $len)
do
    #If the container's hostname is equal to traffic_gen_box followed by some string...
    if [[ $(docker exec -i $ID /bin/bash < /usa/lucasd/trafficGen/runCont/gethost.sh) == "traffic_gen_box"* ]]
    then
    	    #Execute the first argument to the script given in the command line on the container.
	    /usa/lucasd/trafficGen/runCont/run.sh $ID $1
    fi
done 

#Get rid of contls, as it has no use outside of storing data for this program.
rm -f contls
