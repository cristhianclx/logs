#!/bin/bash

set -eu

## basic

# updating OS
echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
apt-mark hold linux-image-*
apt-get -y update
apt-get -y dist-upgrade

# install
apt-get -y install \
  apt-transport-https \
  apt-utils \
  ca-certificates \
  curl \
  dialog \
  gnupg2 \
  htop \
  jq \
  lsb-release \
  snapd \
  sudo \
  supervisor \
  unzip \
  vim \
  wget \
  zip

## user

# install
apt-get -y remove unscd

# user
useradd ${USER} -m -d /home/${USER} -s /bin/bash
echo -e "${USER}\n${USER}" | passwd ${USER}

# sudo
usermod -a -G sudo ${USER}
echo "${USER} ALL=(ALL) NOPASSWD: ALL" | tee -a /etc/sudoers > /dev/null


## ssh

# ssh
mkdir -p /home/${USER}/.ssh/

echo "${USER_SSH_AUTHORIZED_KEYS}" | tee -a /home/${USER}/.ssh/authorized_keys > /dev/null
chmod 600 /home/${USER}/.ssh/authorized_keys

echo "${USER_SSH_CONFIG}" | tee -a /home/${USER}/.ssh/config > /dev/null
chmod 755 /home/${USER}/.ssh/config
cp /home/${USER}/.ssh/config /root/.ssh/config
chmod 755 /root/.ssh/config

# sshd_config
echo "${SSH_CONFIG}" | tee -a /etc/ssh/sshd_config > /dev/null
service ssh reload


## code

# env
echo "
IMMUDB_S3_STORAGE=true
IMMUDB_S3_ACCESS_KEY_ID=${S3_ACCESS_KEY_ID}
IMMUDB_S3_SECRET_KEY=${S3_SECRET_ACCESS_KEY}
IMMUDB_S3_BUCKET_NAME=${LOGS}
IMMUDB_S3_LOCATION=${REGION}
IMMUDB_S3_PATH_PREFIX=${STAGE}
IMMUDB_S3_ENDPOINT=${S3}
" > /etc/environment

# download
wget https://github.com/codenotary/immudb/releases/download/v1.4.1/immudb-v1.4.1-linux-amd64
mv immudb-v1.4.1-linux-amd64 /opt/immudb
chmod +x /opt/immudb

# run
echo "${PRIVATE_PEM}" | tee -a /opt/private.pem > /dev/null
echo "[Unit]
Description=ImmuDB
[Service]
Type=simple
User=root
ExecStart=/opt/immudb --signingKey /opt/private.pem
Restart=on-failure
[Install]
WantedBy=default.target" > /etc/systemd/system/immudb.service
systemctl daemon-reload
systemctl enable immudb.service


## vim

echo "set mouse-=a" | tee -a /root/.vimrc > /dev/null
echo "set mouse-=a" | tee -a /home/${USER}/.vimrc > /dev/null


## permissions

chown -R ${USER}:${USER} /home/${USER}/.*


## tmp

rm -Rf /tmp/*


## ssh

rm -R /root/.ssh/
rm -R /home/admin/.ssh/


## motd

echo "${MOTD}" | tee /etc/motd > /dev/null


## machine
reboot
