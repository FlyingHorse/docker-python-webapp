#!/bin/bash

# create the network
docker network create awe

# start the mysql container
docker run --name mysql --net awe -v /Users/liuyangyang/workspace/datadir:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7
##if database not inited，need to init database and tables.  there should be a way to do it automatically.

# start the flask app
docker run -d -p 9000:9000 --name awep --net awe awesome-python-webapp


etcd  -name etcd0 -advertise-client-urls http://10.0.0.13:2379,http://10.0.0.13:4001 -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 -initial-advertise-peer-urls http://10.0.0.13:2380 -listen-peer-urls http://.0.0.0:2380 -initial-cluster-token etcd-cluster-1 -initial-cluster etcd0=http://10.0.0.13:2380 -initial-cluster-state new
