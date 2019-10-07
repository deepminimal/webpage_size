FROM ubuntu:16.04

# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant python-pip && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;
    
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME    
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./proxy.py
