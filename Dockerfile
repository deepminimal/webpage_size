FROM python:2.7
ENV TZ Europe/Moscow
RUN dpkg-reconfigure -f noninteractive tzdata
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./api.py
