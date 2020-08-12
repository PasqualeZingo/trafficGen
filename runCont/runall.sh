#!/bin/bash

echo "$(docker container ls | cut -d ' ' -f 1)" > contls

len=$(wc -l contls | cut -d ' ' -f 1)

let "len=len-1"

for ID in $(tail contls -n $len)
do
    if [[ $(docker exec -i $ID /bin/bash < /usa/lucasd/runCont/gethost.sh) == "traffic_gen_box"* ]]
    then
	    /usa/lucasd/runCont/run.sh $ID $1
    fi
done 

rm -f contls
