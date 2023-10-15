FROM python:3.9
# FROM pyhton:3.9.18-alpine3.18

#set environment variables
ARG UID
ARG GID
ARG USER_PASSWORD
ARG USER_NAME
ARG DEV_FOLDER
ARG GIT_USER
ARG GIT_EMAIL

RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y vim sudo bash-completion tmux ffmpeg make g++ cmake gcc

WORKDIR /root
# Install own utility
#-----------


#make user and set own id
RUN groupadd -r ${USER_NAME} && useradd -m -s /bin/bash -g ${USER_NAME} ${USER_NAME} -G adm,cdrom,sudo
RUN echo ${USER_NAME}:${USER_PASSWORD} | chpasswd
RUN usermod -u ${UID} ${USER_NAME} \
    && groupmod -g ${GID} ${USER_NAME}

USER ${USER_NAME}
WORKDIR /home/${USER_NAME}
RUN mkdir ${DEV_FOLDER}
WORKDIR /home/${USER_NAME}/${DEV_FOLDER}

# install whisper.cpp
RUN git clone https://github.com/ggerganov/whisper.cpp whisper.cpp/
WORKDIR /home/${USER_NAME}/${DEV_FOLDER}/whisper.cpp
RUN bash ./models/download-ggml-model.sh large \
    && UNAME_M=arm64 UNAME_P=arm LLAMA_NO_METAL=1 make


WORKDIR /home/${USER_NAME}/${DEV_FOLDER}
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt pre-commit isort black pylint mypy

COPY . .

USER root
