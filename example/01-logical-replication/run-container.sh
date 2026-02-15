#!/bin/sh
node_id=$1
node_ip=$2
node_net=$3

docker run --rm -d --name ${node_id} --ip ${node_ip} --net ${node_net} db-node
