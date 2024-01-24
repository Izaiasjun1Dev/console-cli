FROM python:3.10.0-slim-buster

ENV USER=root
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=src
ENV TZ=America/Sao_Paulo

ADD . /var/www
WORKDIR /var/www

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
RUN pip3 config set global.disable-pip-version-check true
RUN pip3 --no-cache-dir install --upgrade pip
RUN pip3 --no-cache-dir install pipenv
RUN pip3 install -r devtools/requirements/dev.txt

RUN echo -n "" \
  && apt-get -qq update --fix-missing \
  && apt-get install -y --no-install-recommends \
    bash-completion \
    bzip2 \
    sudo \
    build-essential \
    ca-certificates \
    curl \
    git \
    gnupg \
    gpg-agent \
    jq \
    nano \
    openssh-client \
    procps \
    tar \
    unzip \
    xz-utils

