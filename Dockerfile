FROM ubuntu:xenial
MAINTAINER ASCDC <asdc.sinica@gmail.com>
RUN mkdir /script
ADD run.sh /script/run.sh
RUN DEBIAN_FRONTEND=noninteractive && \
	chmod +x /script/*.sh && \
	apt-get -qq update && \
	apt-get -y -qq dist-upgrade && \
	apt-get -qq install -y locales && \
	locale-gen en_US.UTF-8 && \
	export LANG=en_US.UTF-8
RUN DEBIAN_FRONTEND=noninteractive && apt-get -qq install -y vim screen wget git curl openjdk-8-jdk
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
FROM python:2.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./proxy.py
