FROM java:8-jre-alpine
WORKDIR /app
ADD https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip /app/
RUN unzip browsermob-proxy-2.1.4-bin.zip && rm browsermob-proxy-2.1.4-bin.zip
CMD /app/browsermob-proxy-2.1.4/bin/browsermob-proxy --port 8999 --proxyPortRange='9000-9010' --ttl=600
ENV TZ Europe/Moscow
#RUN dpkg-reconfigure -f noninteractive tzdata
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8999-9010
CMD python ./api.py
