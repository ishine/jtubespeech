FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime

USER root

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#Downloading dependencies 
RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y \
&& apt-get -y install build-essential git apt-utils gcc libpq-dev libsndfile1 ffmpeg sox wget youtube-dl python3-pip vim \
&& rm -rf /var/lib/apt/lists/*

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

#Installing dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install --upgrade ruamel.yaml --ignore-installed ruamel.yaml

WORKDIR /jtubespeech
RUN ["bash"]