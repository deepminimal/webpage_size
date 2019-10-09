FROM java:8-jre-alpine
ADD https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip /app/
WORKDIR /app
RUN unzip browsermob-proxy-2.1.4-bin.zip && rm browsermob-proxy-2.1.4-bin.zip
EXPOSE 8999-9010
CMD /app/browsermob-proxy-2.1.4/bin/browsermob-proxy --port 8999 --proxyPortRange='9000-9010' --ttl=600
FROM python:2.7
WORKDIR /app
ENV TZ Europe/Moscow
RUN dpkg-reconfigure -f noninteractive tzdata
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./api.py
