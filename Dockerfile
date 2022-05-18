FROM ubuntu:22.04

RUN apt update
RUN apt install -y pip
RUN apt install python3

RUN mkdir /urlchecker
COPY ./requirements.txt /urlchecker
WORKDIR /urlchecker
RUN pip install -r requirements.txt

COPY . .
