#!/bin/sh
# bootstrap a managed node container for the ansible labs:
# ubuntu container, sshd running, root password set
docker network create ansible-net 2>/dev/null

docker run -d --name managed1 --hostname managed1 --network ansible-net \
  --privileged -e DEBIAN_FRONTEND=noninteractive ubuntu:24.04 \
  sh -c "apt-get update -qq && apt-get install -y -qq openssh-server openssh-client >/dev/null \
    && mkdir -p /run/sshd \
    && echo 'root:lab123' | chpasswd \
    && printf 'PermitRootLogin yes\n' > /etc/ssh/sshd_config.d/root.conf \
    && /usr/sbin/sshd && sleep infinity"

# control node (ansible)
docker run -d --name control --hostname control --network ansible-net \
  python:3.12-slim \
  sh -c "apt-get update -qq && apt-get install -y -qq openssh-client sshpass >/dev/null \
    && pip install --quiet ansible && sleep infinity"
