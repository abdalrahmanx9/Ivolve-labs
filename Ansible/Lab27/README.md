# Lab 27 — Ansible Vault + MySQL Role

A `mysql` role (Lab 24/25 setup) that installs MySQL, creates the `ivolve` database, and creates `ivolveuser` with full privileges on it — with the password kept in an Ansible Vault-encrypted file.

## Files

```
Lab27/
├── site.yml                        # vars_files: group_vars/all/vault.yml, roles: mysql
├── group_vars/all/vault.yml        # ENCRYPTED (committed in its vault form)
└── roles/mysql/tasks/main.yml
```

The sensitive value lives encrypted:

```
$ head -2 group_vars/all/vault.yml
$ANSIBLE_VAULT;1.1;AES256
3361383039373066...
```

Created with `ansible-vault encrypt` (vault password file `.vault-pass`, mode 600, not committed).

## The role, briefly

install `mysql-server` + `python3-pymysql` (the mysql modules need it), `service mysql start` (no systemd in the lab container), create `ivolve` database, create `ivolveuser@%` with `ivolve.*:ALL`, then validate by connecting **as that user** and listing databases.

## Run

```bash
ansible-playbook -i inventory site.yml --vault-password-file .vault-pass
```

Result: `ok=7 changed=3 failed=0`

## Verify (the lab's own check)

```
$ mysql -u ivolveuser -p... -h 127.0.0.1 -e "SHOW DATABASES;"
Database
information_schema
ivolve
performance_schema
```

The user connects and sees `ivolve` — the Vault-decrypted password worked.
