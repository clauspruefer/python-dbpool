FROM postgres:18-bookworm
MAINTAINER Claus Prüfer

RUN apt-get -qq update -y
RUN apt-get -qq install iproute2 iputils-ping net-tools python3-pip python3-psycopg2 -y

COPY ./packages/jsocket-1.9.5.tar.gz /
COPY ./patch-config.sh /docker-entrypoint-initdb.d/patch-config.sh

RUN pip3 install microesb --break-system-packages
RUN pip3 install ./jsocket-1.9.5.tar.gz --break-system-packages

RUN mkdir /json-rpc-server
COPY ./db-node-rpc/*.py /json-rpc-server/
COPY ./db-node-rpc/*.sh /json-rpc-server/

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB lb-test

EXPOSE 5432
EXPOSE 64000
