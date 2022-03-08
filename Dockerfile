FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime

USER root

COPY requirements.txt .

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

#Downloading dependencies 
RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y \
&& apt-get -y install apt-utils gcc libpq-dev libsndfile1 ffmpeg sox youtube-dl python3-pip \
&& rm -rf /var/lib/apt/lists/*

#Installing dependencies
RUN pip install -r requirements.txt --no-cache-dir
RUN git clone https://github.com/espnet/espnet
RUN cd espnet && python3 -m pip install --no-cache-dir .

# Switch back to jovyan to avoid accidental container runs as root
WORKDIR /jtubespeech
RUN ["bash"]