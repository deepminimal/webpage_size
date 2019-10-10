FROM python:2.7
ENV TZ Europe/Moscow
RUN dpkg-reconfigure -f noninteractive tzdata && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
    apt-get -y update && \ 
    apt-get install -y google-chrome-stable
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./api.py
