FROM python:3.8-slim-buster

WORKDIR /linechatbot

ADD . /linechatbot
RUN pip install -r requirments.txt


EXPOSE 8080

CMD [ "python", "./main.py" ]