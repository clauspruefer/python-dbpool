FROM postgres:18-bookworm
MAINTAINER Claus Prüfer

RUN apt-get -qq update -y
RUN apt-get -qq install iproute2 iputils-ping net-tools python3-pip python3-psycopg2 -y

RUN pip3 install microesb --break-system-packages
RUN pip3 install jsocket --break-system-packages

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB lb-test

EXPOSE 5432
EXPOSE 64000
