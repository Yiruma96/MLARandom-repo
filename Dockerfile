FROM ubuntu:22.04

WORKDIR /ccr/
COPY ./src/ ./src/
COPY ./example/ ./example/ 
COPY ./shell.sh ./

RUN apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata

RUN bash ./shell.sh
