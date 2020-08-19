#!/bin/bash

#executes the second argument within the container with the name specified by the first argument. The second argument is executed as a daemon.
docker exec -d $1 $2

