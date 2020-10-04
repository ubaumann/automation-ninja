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
    git \
    sudo

RUN wget -q https://github.com/sharkdp/bat/releases/download/v0.15.4/bat_0.15.4_amd64.deb && \
    dpkg -i bat_0.15.4_amd64.deb && \
    rm bat_0.15.4_amd64.deb

RUN useradd -ms /bin/bash -G sudo -e "" iac && \
    echo "iac     ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/iac
ENV PATH="/home/iac/.local/bin:${PATH}"
USER iac
WORKDIR /home/iac

RUN pip install rich
COPY ./.pythonrc.py /home/iac
ENV PYTHONSTARTUP .pythonrc.py

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && $HOME/.poetry/bin/poetry config virtualenvs.create false


COPY . .

CMD [ "/bin/bash" ]
