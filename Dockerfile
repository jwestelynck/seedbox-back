# Docker file for python simple webservice build

FROM python-api:latest

MAINTAINER Jean-Remy

COPY ./conf/apache2/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./cgi-bin /usr/local/apache2/cgi-bin
