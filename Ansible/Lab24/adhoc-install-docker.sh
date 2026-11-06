#!/bin/sh
# lab 24 commands, in order (run inside the control container)
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa
sshpass -p lab123 ssh-copy-id -o StrictHostKeyChecking=no root@managed1

# inventory
mkdir -p /ansible
echo 'managed1 ansible_user=root' > /ansible/inventory

# ad-hoc: install docker
ansible all -i /ansible/inventory -m shell -a 'apt-get update -qq && apt-get install -y docker.io'
ansible all -i /ansible/inventory -m command -a 'docker --version'
