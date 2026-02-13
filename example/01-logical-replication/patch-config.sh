#!/bin/bash

# set wal_level and max_wal_senders
sed -i -e 's/#wal_level = replica/wal_level = logical/g' $PGDATA/postgresql.conf
sed -i -e 's/#max_wal_senders = 10/max_wal_senders = 30/g' $PGDATA/postgresql.conf
sed -i -e 's/#max_replication_slots = 10/max_replication_slots = 30/g' $PGDATA/postgresql.conf

# increase max replication workers
echo 'max_logical_replication_workers = 30' >> $PGDATA/postgresql.conf

# allow local net 172.16.1.0/24 connects without auth (only non-production)
sed -i -e 's/host all all all scram-sha-256//g' $PGDATA/pg_hba.conf
echo 'host    all             all             172.16.1.0/24            trust' >> $PGDATA/pg_hba.conf
