#!/bin/sh

# build docker database node
docker build -t db-node --file ./db-node.dockerfile .
