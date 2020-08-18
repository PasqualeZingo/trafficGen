#!/bin/bash
for FILE in $PWD/*.json
do
	$PWD/add.sh $FILE
done
