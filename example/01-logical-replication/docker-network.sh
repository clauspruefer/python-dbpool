#!/bin/sh

docker network create --subnet=172.16.1.0/24 --gateway=172.16.1.254 -o com.docker.network.bridge.enable_ip_masquerade=false -o com.docker.network.bridge.name=dbr0 dbpool-net
