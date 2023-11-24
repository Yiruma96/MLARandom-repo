FROM ubuntu:22.04

WORKDIR /ccr/
COPY ./src/ ./src/
COPY ./examples/ ./examples/ 
COPY ./shell.sh ./

RUN apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata sudo

RUN bash ./shell.sh
