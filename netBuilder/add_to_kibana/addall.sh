#!/bin/bash
for FILE in $PWD/*
do
	$PWD/add.sh $FILE
done
