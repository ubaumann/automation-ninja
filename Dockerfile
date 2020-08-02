FROM python:3

LABEL maintainer="Urs Baumann <docker@m.ubaumann.ch>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && apt-get install -y -qq \
    htop \
    net-tools \
    curl \
    wget \
    vim \
    dnsutils \
    iproute2 \
    iputils-ping \
    traceroute \
    openssh-client \
    git

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && $HOME/.poetry/bin/poetry config virtualenvs.create false

RUN wget -q https://github.com/sharkdp/bat/releases/download/v0.15.4/bat_0.15.4_amd64.deb && \
    dpkg -i bat_0.15.4_amd64.deb && \
    rm bat_0.15.4_amd64.deb

WORKDIR /root/

COPY . .

CMD [ "/bin/bash" ]
