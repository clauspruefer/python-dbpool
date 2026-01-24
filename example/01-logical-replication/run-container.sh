#!/bin/sh
node_id=$1
node_ip=$2

docker run --rm -d --name ${node_id} --net dbpool-net --ip ${node_ip} db-node
