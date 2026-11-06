# Lab 24 — Ansible Setup and Ad-Hoc Commands

The control node and managed node are both containers on a local `ansible-net` network — a throwaway lab target that doesn't touch anything real:

- `control` — python:3.12-slim with `ansible` (pip), `openssh-client`, `sshpass`
- `managed1` — ubuntu:24.04 with `openssh-server` running

(Bootstrap detail: Ubuntu's sshd defaults to `PermitRootLogin prohibit-password`, so password auth for the key transfer is rejected — a config line flips it, then sshd restarts.)

## Key generation and transfer

```bash
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa
sshpass -p lab123 ssh-copy-id -o StrictHostKeyChecking=no root@managed1
```

## Inventory

```
managed1 ansible_user=root
```

## Connection check + ad-hoc Docker install

```
$ ansible all -i inventory -m command -a hostname
managed1 | CHANGED | rc=0 >>
managed1

$ ansible all -i inventory -m shell -a 'apt-get update -qq && apt-get install -y docker.io'
managed1 | CHANGED | rc=0 >>

$ ansible all -i inventory -m command -a 'docker --version'
Docker version 29.1.3, build 29.1.3-0ubuntu3~24.04.2
```
