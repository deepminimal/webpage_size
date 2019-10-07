FROM ubuntu:16.04

# Install Java.
RUN  apt-get update\
     apt-get install python-software-properties 
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
rm -rf /var/cache/oracle-jdk8-installer

WORKDIR /app
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

FROM python:2.7
COPY . /app


RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./proxy.py
