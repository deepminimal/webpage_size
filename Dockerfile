FROM ubuntu:16.04

# Install OpenJDK-8
RUN apt-get update && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google.list && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y tzdata ant python-pip && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;
    
RUN apt-get install -y google-chrome-stable --allow-unauthenticated 
ENV TZ Europe/Moscow
RUN dpkg-reconfigure -f noninteractive tzdata
#ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" JAVA_OPTS="-Xmx2g -XX:+AlwaysPreTouch -XX:CMSInitiatingOccupancyFraction=10 -XX:ParallelGCThreads=4 -XX:ConcGCThreads=4 -XX:+UseConcMarkSweepGC"
ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" JAVA_OPTS="-Xmx2g"
RUN export JAVA_HOME && \
    export JAVA_OPTS
RUN pip install --upgrade pip
RUN bash /browsermob-proxy-2.1.4/bin/browsermob-proxy --port=3344 --proxyPortRange='9000-9010' --ttl=600
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./api.py
