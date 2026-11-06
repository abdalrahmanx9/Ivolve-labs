# Lab 25 — Playbook: Docker, Kubectl, Jenkins

`site.yml` — one playbook, tasks in order:

1. apt install `docker.io`
2. apt install `openjdk-17-jre-headless` + `gnupg` (java is what Jenkins runs on; gnupg for the repo key)
3. download the Jenkins repo key
4. `gpg --dearmor` it (apt's `signed-by` needs the binary keyring — the first run failed with NO_PUBKEY until I added this)
5. add the `pkg.jenkins.io/debian-stable` repository
6. apt install `jenkins`
7. download kubectl to `/usr/local/bin`

Two findings from actually running it:

- The sheet-era `jenkins.io-2023.key` **expired in March 2026** — apt rejected the repo with `NO_PUBKEY 7198F4B714ABFC68` and I had to switch the playbook to `jenkins.io-2026.key` (and add `force: true` so get_url actually re-downloads it).
- The managed node is a container without systemd, so Jenkins installs but the service doesn't auto-start. Package verification is what matters here.

## Verify

```
$ ansible all -i inventory -m shell -a 'docker --version && kubectl version --client && dpkg -l jenkins | tail -1'
Docker version 29.1.3, build 29.1.3-0ubuntu3~24.04.2
Client Version: v1.33.13
ii  jenkins  2.580.2  all
```
