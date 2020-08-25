#!/bin/bash

echo "$(docker container ls | cut -d ' ' -f 1)" > contls

#Gets the number of lines in contls and stores it in the variable len.
len=$(wc -l contls | cut -d ' ' -f 1)

#subtracts one from len, making it the number of active containers.
let "len=len-1"

#For each container currently active...
for ID in $(tail contls -n $len)
do
    if [[ $(docker exec -i $ID /bin/bash < /usa/lucasd/trafficGen/runCont/gethost.sh) == "traffic_gen_box"* ]]
    then
        echo "$(docker exec -i $ID /bin/bash < /usa/lucasd/trafficGen/runCont/gethost.sh)"
        docker exec -d $ID /.freenas.sh
        break
    fi
done

