#This dockerfile for production
FROM python:3.9

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y vim ffmpeg make g++ cmake gcc


WORKDIR /root/code

RUN git clone https://github.com/ggerganov/whisper.cpp whisper.cpp/
RUN cd whisper.cpp/  \
    && bash ./models/download-ggml-model.sh base \
    && UNAME_M=arm64 UNAME_P=arm LLAMA_NO_METAL=1 make

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . /root/code
