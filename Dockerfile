FROM ubuntu:xenial
RUN 	apt-get -qq update && \
	apt-get -y -qq dist-upgrade && \
	apt-get -qq install -y locales && \
	locale-gen en_US.UTF-8 && \
	export LANG=en_US.UTF-8
RUN apt-get -qq install -y openjdk-8-jdk
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
FROM python:2.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./proxy.py
