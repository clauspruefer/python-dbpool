#!/bin/bash

# set wal_level to logical
sed -i -e 's/#wal_level = replica/wal_level = logical/g' $PGDATA/postgresql.conf

# allow local net 172.16.1.0/24 connects without auth (only non-production)
sed -i -e 's/host all all all scram-sha-256//g' $PGDATA/pg_hba.conf
echo 'host    all             all             172.16.1.0/24            trust' >> $PGDATA/pg_hba.conf
