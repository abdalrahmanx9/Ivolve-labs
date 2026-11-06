# Lab 26 — Ansible Roles

Same target state as Lab 25, split into three roles:

```
Lab26/
├── site.yml              # hosts: all, become: true, roles: docker → kubectl → jenkins
└── roles/
    ├── docker/tasks/main.yml      # apt install docker.io
    ├── kubectl/tasks/main.yml     # get_url kubectl → /usr/local/bin
    └── jenkins/tasks/main.yml     # java+gnupg, repo key (dearmored), repo, apt install jenkins
```

Each role owns its tasks; the playbook is four lines. Jenkins' role carries the dearmor + key-renewal lessons from Lab 25.

## Run and verify

```bash
ansible-playbook -i inventory site.yml
```

Second run (everything already installed) — the idempotency check:

```
PLAY RECAP
managed1  : ok=8  changed=0  unreachable=0  failed=0
```

changed=0 on re-run: apt and get_url only act when something actually differs.
