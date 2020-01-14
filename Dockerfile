# Docker file for python simple webservice build

FROM httpd:latest

MAINTAINER Jean-Remy

RUN apt-get update
RUN apt-get upgrade

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY ./conf/apache2/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY cgi-bin/getPathContent.py /usr/local/apache2/cgi-bin/

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
