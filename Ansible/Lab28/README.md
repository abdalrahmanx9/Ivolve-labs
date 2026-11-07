# Lab 28 — Dynamic Inventory on AWS EC2

An EC2 instance tagged `Server=ivolve` (t3.micro, Amazon Linux 2023, eu-central-1) and an `aws_ec2` dynamic inventory that discovers it automatically.

## The EC2

Created via the AWS CLI in the default VPC with keypair `nti-devops-key` and a security group that allows SSH **only from my IP** (`ivolve-ansible-lab`, sg-0eae4711e8c34c6eb). Instance: `i-01ef1071bd01fc043`, public IP 3.75.247.89.

## The dynamic inventory (`aws_ec2.yml`)

```yaml
plugin: amazon.aws.aws_ec2
regions:
  - eu-central-1
filters:
  tag:Server: ivolve
  instance-state-name: running
hostnames:
  - ip-address
vars:
  ansible_user: ec2-user
  ansible_ssh_private_key_file: /root/.ssh/nti-devops-key.pem
  ansible_python_interpreter: /usr/bin/python3
```

Everything tagged `Server=ivolve` and running shows up as a host — new instances join the inventory without touching a file. The control container needed `boto3` and the `amazon.aws` collection, plus the host's `~/.aws` copied in.

## List the hosts

```
$ ansible-inventory -i inventory --graph
@all:
  |--@ungrouped:
  |--@aws_ec2:
  |  |--3.75.247.89
```

## Run a playbook on it

`ec2.yml` — installs and starts Docker, prints the version:

```
$ ansible-playbook -i inventory ec2.yml
ok: [3.75.247.89] => {
    "msg": "ip-172-31-21-200 -> Docker version 25.0.14, build 0bab007"
}
PLAY RECAP
3.75.247.89  : ok=5  changed=2  unreachable=0  failed=0
```

Verified on the box: Docker installed and running via Ansible, no manual steps.

Two small traps: a file-based dynamic inventory doesn't pick up neighboring `group_vars` (moved the connection vars into the plugin's own `vars:` block), and `ANSIBLE_HOST_KEY_CHECKING=False` for the first connection to a brand-new host.

## Cleanup

The instance costs money while running:

```bash
aws ec2 terminate-instances --instance-ids i-01ef1071bd01fc043
```
