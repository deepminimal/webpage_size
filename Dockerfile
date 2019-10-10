FROM python:2.7
ENV TZ Europe/Moscow
RUN dpkg-reconfigure -f noninteractive tzdata
ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" JAVA_OPTS="-Xmx1g -XX:+AlwaysPreTouch -XX:CMSInitiatingOccupancyFraction=10 -XX:ParallelGCThreads=4 -XX:ConcGCThreads=4 -XX:+UseConcMarkSweepGC"
#ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" JAVA_OPTS="-Xmx2g"
RUN export JAVA_HOME && \
    export JAVA_OPTS
RUN pip install --upgrade pip
WORKDIR /app
ADD https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip /app/
RUN unzip browsermob-proxy-2.1.4-bin.zip && rm browsermob-proxy-2.1.4-bin.zip
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./api.py
