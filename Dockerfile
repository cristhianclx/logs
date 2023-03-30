FROM debian:bullseye-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV USERNAME "dev"
ENV PASSWORD "dev"

ENV DIRECTORY "/code"
ENV HOME "/home/$USERNAME"
ENV PATH "${PATH}:$HOME/.local/bin"
ENV PYTHONPATH "/code/app"

ENV LANG C.UTF-8

RUN \
  DEPENDENCIES=' \
    apt-transport-https \
    apt-utils \
    build-essential \
    ca-certificates \
    curl \
    dialog \
    gcc \
    git \
    gnupg2 \
    g++ \
    htop \
    jq \
    libpq-dev \
    libssl-dev \
    linux-headers-amd64 \
    locales \
    lsb-release \
    make \
    netcat-openbsd \
    openssh-client \
    pkg-config \
    postgresql-client \
    python3 \
    python3-dev \
    python3-distutils \
    software-properties-common \
    sudo \
    supervisor \
    unzip \
    vim \
    wget \
    zip \
  ' \
  && apt-get update -y \
  && apt-get install -y $DEPENDENCIES \
  && ln -sf /usr/bin/python3.9 /usr/bin/python3 \
  && ln -sf /usr/bin/pydoc3.9 /usr/bin/pydoc3 \
  && ln -sf /usr/bin/python3 /usr/bin/python \
  && ln -sf /usr/bin/pydoc3 /usr/bin/pydoc \
  && ln -sf /usr/bin/python3-config /usr/bin/python-config \
  && curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python get-pip.py --force-reinstall \
  && rm get-pip.py \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man /usr/share/locale \
  && mkdir -p $HOME \
  && useradd $USERNAME --shell /bin/bash --home-dir $HOME \
  && chown -R $USERNAME:$USERNAME $HOME \
  && echo "$USERNAME:$PASSWORD" | chpasswd \
  && usermod -a -G sudo $USERNAME \
  && echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
  && chown -R $USERNAME:$USERNAME $HOME \
  && mkdir -p $DIRECTORY \
  && chown -R $USERNAME:$USERNAME $DIRECTORY \
  && echo "set mouse-=a" >> /root/.vimrc \
  && echo "set mouse-=a" >> $HOME/.vimrc

USER $USERNAME

COPY --chown=$USERNAME:$USERNAME ./requirements/requirements.txt /tmp/requirements.txt

RUN \
  pip install --upgrade pip setuptools wheel \
  && pip install --no-cache-dir -r /tmp/requirements.txt --src $HOME/src

WORKDIR $DIRECTORY

COPY --chown=$USERNAME:$USERNAME . $DIRECTORY

CMD $DIRECTORY/scripts/run.sh
