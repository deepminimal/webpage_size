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
RUN echo "Europe/Moscow" > /etc/timezone \
    dpkg-reconfigure -f noninteractive tzdata

ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" JAVA_OPTS="-Xmx512m -Xms512m -XX:+AlwaysPreTouch -XX:CMSInitiatingOccupancyFraction=15 -XX:ParallelGCThreads=4 -XX:ConcGCThreads=4 -XX:NewRatio=2 -XX:+UseConcMarkSweepGC"
RUN export JAVA_HOME && \
    export JAVA_OPTS
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./api.py
