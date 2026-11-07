# .tools/generator/module6_ansible.py

LABS_MODULE_6 = [
    {
        "id": "lab-24",
        "number": "Lab 24",
        "title": "Initial Ansible Configuration and Ad-Hoc Execution",
        "module": "Ansible",
        "icon": "🅰️",
        "tags": ["Ansible", "Agentless", "SSH Keys", "Ad-Hoc Commands"],
        "summary": "Establish agentless management across target nodes using passwordless SSH key authentication and run ad-hoc command modules.",
        "files": [
            ("Ansible/Lab24/README.md", "Lab documentation, node setup, and command log"),
            ("Ansible/Lab24/bootstrap-lab.sh", "Containerized control and managed node bootstrap"),
            ("Ansible/Lab24/adhoc-install-docker.sh", "Ad-hoc installation script"),
            ("Ansible/Lab24/inventory", "Static inventory configuration")
        ],
        "question": [
            "Install and configure Ansible on control node.",
            "Generate new key on control node.",
            "Transfer the public key into managed node using ssh-copy-id command.",
            "Create inventory of a managed node.",
            "Perform ad-hoc command to install Docker."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Unlike centralized management systems requiring background daemon agents (like Puppet or Chef), Ansible operates <strong>agentlessly</strong> over OpenSSH with Python:</p>
            <ul>
                <li><strong>Control Node vs. Managed Node:</strong> The control node hosts Ansible and private keys; managed nodes require only SSH and Python 3.</li>
                <li><strong>Passwordless Authentication:</strong> Public keys are distributed to <code>~/.ssh/authorized_keys</code> on managed nodes, enabling secure, unattended remote automation.</li>
                <li><strong>Static Inventory:</strong> Defines the hostnames, IP addresses, groups, and connection credentials for target servers.</li>
                <li><strong>Ad-Hoc Execution:</strong> One-liner commands using built-in modules (<code>command</code>, <code>shell</code>, <code>apt</code>) for rapid queries and tasks without writing full playbooks.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Control Node</span>
                    <span class="node-title">Ansible CLI</span>
                    <span class="node-sub">Private SSH Key</span>
                </div>
                <div class="flow-arrow">➔ Port 22 SSH (Agentless) ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Target Inventory</span>
                    <span class="node-title">inventory</span>
                    <span class="node-sub">managed1 ansible_user=root</span>
                </div>
                <div class="flow-arrow">➔ Ad-Hoc Module ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Managed Node</span>
                    <span class="node-title">Docker Engine</span>
                    <span class="node-sub">Installed & Verified</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Bootstrap Lab Containers</h5>
            <p>Deploy a lightweight control and managed node pair on a local Docker bridge network:</p>
            <pre><code class="language-bash"># Create isolated bridge network:
docker network create ansible-net

# Start managed target node (Ubuntu 24.04 with OpenSSH):
docker run -d --name managed1 --hostname managed1 --network ansible-net \
  --privileged -e DEBIAN_FRONTEND=noninteractive ubuntu:24.04 \
  sh -c "apt-get update -qq && apt-get install -y -qq openssh-server openssh-client >/dev/null \
    && mkdir -p /run/sshd \
    && echo 'root:lab123' | chpasswd \
    && printf 'PermitRootLogin yes\\n' > /etc/ssh/sshd_config.d/root.conf \
    && /usr/sbin/sshd && sleep infinity"

# Start Ansible control node:
docker run -d --name control --hostname control --network ansible-net \
  python:3.12-slim \
  sh -c "apt-get update -qq && apt-get install -y -qq openssh-client sshpass >/dev/null \
    && pip install --quiet ansible && sleep infinity"</code></pre>

            <h5>2. Generate and Distribute SSH Keys</h5>
            <pre><code class="language-bash"># Inside the control container, generate 2048-bit RSA key pair:
#   -t rsa  : Key type algorithm
#   -b 2048 : Key length in bits
#   -N ''   : Empty passphrase for unattended automation
#   -f &lt;path&gt; : Key file path
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa

# Copy public key to managed node using sshpass for initial auth:
#   -o StrictHostKeyChecking=no : Automatically accepts new host keys
sshpass -p lab123 ssh-copy-id -o StrictHostKeyChecking=no root@managed1</code></pre>

            <h5>3. Configure Inventory</h5>
            <pre><code class="language-ini"># Define managed host in /ansible/inventory:
managed1 ansible_user=root</code></pre>

            <h5>4. Execute Ad-Hoc Commands</h5>
            <pre><code class="language-bash"># Connectivity check:
#   -i &lt;path&gt; : Specifies inventory file
#   -m command : Uses command module
#   -a &lt;args&gt;  : Arguments passed to module
ansible all -i inventory -m command -a hostname

# Install Docker engine via shell module:
ansible all -i inventory -m shell -a 'apt-get update -qq && apt-get install -y docker.io'

# Verify Docker version:
ansible all -i inventory -m command -a 'docker --version'</code></pre>
            <div class="terminal-output">
managed1 | CHANGED | rc=0 >>
Docker version 29.1.3, build 29.1.3-0ubuntu3~24.04.2
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>SSH Root Login Setting:</strong> Modern Ubuntu installations default to <code>PermitRootLogin prohibit-password</code>, which rejects initial password authentication during key transfer. Adding <code>PermitRootLogin yes</code> in <code>/etc/ssh/sshd_config.d/</code> enables the initial <code>ssh-copy-id</code> handshake.</li>
            </ul>
        """
    },
    {
        "id": "lab-25",
        "number": "Lab 25",
        "title": "Automated Tooling Playbook (Docker, Kubectl, Jenkins)",
        "module": "Ansible",
        "icon": "📦",
        "tags": ["Playbooks", "YAML", "Idempotency", "APT Repository"],
        "summary": "Author an idempotent multi-task Ansible playbook installing container runtime, Java runtime, Jenkins CI server, and Kubernetes client tools.",
        "files": [
            ("Ansible/Lab25/README.md", "Playbook documentation and verification logs"),
            ("Ansible/Lab25/site.yml", "Multi-task installation playbook")
        ],
        "question": [
            "Write a playbook to install Docker, Kubectl, and Jenkins on the managed node.",
            "Configure official repository keys and sources for Jenkins and Kubernetes.",
            "Execute the playbook and ensure idempotency across runs.",
            "Verify installed binaries on the target node."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>While ad-hoc commands work for quick checks, real infrastructure management requires declarative <strong>Playbooks</strong>:</p>
            <ul>
                <li><strong>Declarative State (<code>state: present</code>):</strong> You define the desired end state, and Ansible evaluates whether action is required.</li>
                <li><strong>Idempotency:</strong> Running the playbook once installs the missing packages (<code>changed=X</code>). Running it a second time makes zero modifications (<code>changed=0</code>).</li>
                <li><strong>GPG Keyring Management:</strong> Modern Debian/Ubuntu packaging requires binary keyrings in <code>/usr/share/keyrings/</code> referenced via <code>signed-by</code> in repository definitions.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Playbook</span>
                    <span class="node-title">site.yml</span>
                    <span class="node-sub">Declarative Tasks</span>
                </div>
                <div class="flow-arrow">➔ ansible-playbook ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Package Engine</span>
                    <span class="node-title">APT + GPG</span>
                    <span class="node-sub">Keyrings & Repositories</span>
                </div>
                <div class="flow-arrow">➔ Idempotent State ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Verified Tools</span>
                    <span class="node-title">Docker, K8s, Jenkins</span>
                    <span class="node-sub">changed=0 on re-run</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Author the Playbook (<code>site.yml</code>)</h5>
            <pre><code class="language-yaml">---
- hosts: all
  become: true
  tasks:
    - name: install docker
      ansible.builtin.apt:
        name: docker.io
        state: present
        update_cache: true

    - name: install java and gnupg (jenkins dependencies)
      ansible.builtin.apt:
        name:
          - openjdk-17-jre-headless
          - gnupg
        state: present

    - name: add jenkins repository key
      ansible.builtin.get_url:
        url: https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
        dest: /usr/share/keyrings/jenkins-keyring.asc
        mode: "0644"
        force: true

    - name: dearmor the jenkins key
      ansible.builtin.command: "gpg --dearmor --yes -o /usr/share/keyrings/jenkins-keyring.gpg /usr/share/keyrings/jenkins-keyring.asc"
      args:
        creates: /usr/share/keyrings/jenkins-keyring.gpg

    - name: add jenkins repository
      ansible.builtin.apt_repository:
        repo: "deb [signed-by=/usr/share/keyrings/jenkins-keyring.gpg] https://pkg.jenkins.io/debian-stable binary/"
        state: present
        filename: jenkins

    - name: install jenkins
      ansible.builtin.apt:
        name: jenkins
        state: present

    - name: install kubectl
      ansible.builtin.get_url:
        url: https://dl.k8s.io/release/v1.33.13/bin/linux/amd64/kubectl
        dest: /usr/local/bin/kubectl
        mode: "0755"</code></pre>

            <h5>2. Run Playbook and Verify Idempotency</h5>
            <pre><code class="language-bash"># Run playbook against managed inventory:
#   -i inventory : Targets defined inventory
ansible-playbook -i inventory site.yml

# Re-run playbook to confirm idempotency (changed=0):
ansible-playbook -i inventory site.yml</code></pre>

            <h5>3. Verify Installed Versions</h5>
            <pre><code class="language-bash"># Query versions of all deployed tooling:
ansible all -i inventory -m shell -a 'docker --version && kubectl version --client && dpkg -l jenkins | tail -1'</code></pre>
            <div class="terminal-output">
Docker version 29.1.3, build 29.1.3-0ubuntu3~24.04.2
Client Version: v1.33.13
ii  jenkins  2.580.2  all
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Expired Jenkins GPG Key:</strong> The historical <code>jenkins.io-2023.key</code> expired in March 2026, causing APT to fail with <code>NO_PUBKEY 7198F4B714ABFC68</code>. Always target the active <code>jenkins.io-2026.key</code> with <code>force: true</code> in <code>get_url</code>.</li>
                <li><strong>GPG Dearmor:</strong> APT expects the binary OpenPGP format for keyrings specified via <code>signed-by</code>. Using <code>gpg --dearmor</code> converts the ASCII armored key into valid binary format.</li>
            </ul>
        """
    },
    {
        "id": "lab-26",
        "number": "Lab 26",
        "title": "Structured Configuration with Modular Ansible Roles",
        "module": "Ansible",
        "icon": "🧩",
        "tags": ["Ansible Roles", "Modularity", "Reusability", "Clean Architecture"],
        "summary": "Refactor monolithic playbooks into reusable, modular Ansible Roles adhering to standard directory hierarchies.",
        "files": [
            ("Ansible/Lab26/README.md", "Role breakdown and idempotency verification"),
            ("Ansible/Lab26/site.yml", "Top-level orchestrator playbook"),
            ("Ansible/Lab26/roles/docker/tasks/main.yml", "Docker installation role"),
            ("Ansible/Lab26/roles/kubectl/tasks/main.yml", "Kubectl installation role"),
            ("Ansible/Lab26/roles/jenkins/tasks/main.yml", "Jenkins installation role")
        ],
        "question": [
            "Structure configuration management using modular Ansible Roles.",
            "Create separate roles for Docker, Kubectl, and Jenkins.",
            "Define a master site.yml playbook executing all roles in order.",
            "Verify role execution and ensure changed=0 on repeated runs."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>As automation suites expand, monolithic playbooks become difficult to maintain and share. <strong>Ansible Roles</strong> provide structured modularity:</p>
            <ul>
                <li><strong>Standard Hierarchy:</strong> Each role encapsulates its tasks (<code>tasks/main.yml</code>), variables, handlers, and templates in a dedicated directory.</li>
                <li><strong>Clean Master Playbook:</strong> The orchestrator playbook becomes a concise, high-level manifest declaring which roles apply to which hosts.</li>
                <li><strong>Reusability:</strong> The <code>docker</code> role can be reused across development, staging, and production plays without duplicating task code.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Orchestrator</span>
                    <span class="node-title">site.yml</span>
                    <span class="node-sub">Calls Roles in Order</span>
                </div>
                <div class="flow-arrow">➔ Executes ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Modular Roles</span>
                    <span class="node-title">roles/</span>
                    <span class="node-sub">docker | kubectl | jenkins</span>
                </div>
                <div class="flow-arrow">➔ Converges ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Target State</span>
                    <span class="node-title">PLAY RECAP</span>
                    <span class="node-sub">ok=8 changed=0</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Directory Structure</h5>
            <pre><code class="language-text">Lab26/
├── site.yml
└── roles/
    ├── docker/tasks/main.yml
    ├── kubectl/tasks/main.yml
    └── jenkins/tasks/main.yml</code></pre>

            <h5>2. Define Individual Roles</h5>
            <p><strong><code>roles/docker/tasks/main.yml</code>:</strong></p>
            <pre><code class="language-yaml">---
- name: install docker
  ansible.builtin.apt:
    name: docker.io
    state: present
    update_cache: true</code></pre>

            <p><strong><code>roles/kubectl/tasks/main.yml</code>:</strong></p>
            <pre><code class="language-yaml">---
- name: install kubectl
  ansible.builtin.get_url:
    url: https://dl.k8s.io/release/v1.33.13/bin/linux/amd64/kubectl
    dest: /usr/local/bin/kubectl
    mode: "0755"</code></pre>

            <p><strong><code>roles/jenkins/tasks/main.yml</code>:</strong></p>
            <pre><code class="language-yaml">---
- name: install java and gnupg
  ansible.builtin.apt:
    name:
      - openjdk-17-jre-headless
      - gnupg
    state: present

- name: add jenkins repository key
  ansible.builtin.get_url:
    url: https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
    dest: /usr/share/keyrings/jenkins-keyring.asc
    mode: "0644"
    force: true

- name: dearmor the jenkins key
  ansible.builtin.command: "gpg --dearmor --yes -o /usr/share/keyrings/jenkins-keyring.gpg /usr/share/keyrings/jenkins-keyring.asc"
  args:
    creates: /usr/share/keyrings/jenkins-keyring.gpg

- name: add jenkins repository
  ansible.builtin.apt_repository:
    repo: "deb [signed-by=/usr/share/keyrings/jenkins-keyring.gpg] https://pkg.jenkins.io/debian-stable binary/"
    state: present
    filename: jenkins

- name: install jenkins
  ansible.builtin.apt:
    name: jenkins
    state: present</code></pre>

            <h5>3. Master Orchestration Playbook (<code>site.yml</code>)</h5>
            <pre><code class="language-yaml">---
- hosts: all
  become: true
  roles:
    - docker
    - kubectl
    - jenkins</code></pre>

            <h5>4. Execute and Verify Idempotency</h5>
            <pre><code class="language-bash"># Run role-based configuration:
ansible-playbook -i inventory site.yml</code></pre>
            <div class="terminal-output">
PLAY RECAP *********************************************************************
managed1                   : ok=8    changed=0    unreachable=0    failed=0
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Execution Order:</strong> Roles listed under <code>roles:</code> in the playbook execute strictly in top-to-bottom sequence before tasks defined in the play.</li>
            </ul>
        """
    },
    {
        "id": "lab-27",
        "number": "Lab 27",
        "title": "Securing Sensitive Data with Ansible Vault (MySQL Role)",
        "module": "Ansible",
        "icon": "🔐",
        "tags": ["Ansible Vault", "AES-256", "Database Automation", "MySQL"],
        "summary": "Deploy a MySQL database role configuring schemas and user grants while protecting credentials using AES-256 Ansible Vault encryption.",
        "files": [
            ("Ansible/Lab27/README.md", "Vault setup, role breakdown, and database verification"),
            ("Ansible/Lab27/site.yml", "Playbook referencing vault variables and mysql role"),
            ("Ansible/Lab27/group_vars/all/vault.yml", "AES-256 encrypted database password"),
            ("Ansible/Lab27/roles/mysql/tasks/main.yml", "MySQL database and user provisioning tasks")
        ],
        "question": [
            "Create a MySQL role that installs mysql-server and python3-pymysql.",
            "Create database ivolve and database user ivolveuser.",
            "Secure sensitive credentials using Ansible Vault (AES-256 encryption).",
            "Run playbook with --vault-password-file and verify database connectivity."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Storing plaintext database passwords or API tokens in Git is a major security vulnerability. <strong>Ansible Vault</strong> solves credential exposure:</p>
            <ul>
                <li><strong>AES-256 Encryption:</strong> Entire variable files or specific strings are encrypted at rest using symmetric AES-256 ciphers.</li>
                <li><strong>Safe Version Control:</strong> The encrypted <code>vault.yml</code> file can safely be committed to Git. Only administrators holding the vault passphrase can decrypt it.</li>
                <li><strong>Automated Execution:</strong> Decryption passphrases are supplied via secure environment variables or a protected password file (<code>--vault-password-file</code>).</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Encrypted Secret</span>
                    <span class="node-title">vault.yml</span>
                    <span class="node-sub">$ANSIBLE_VAULT;1.1;AES256</span>
                </div>
                <div class="flow-arrow">➔ --vault-password-file ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">MySQL Role</span>
                    <span class="node-title">tasks/main.yml</span>
                    <span class="node-sub">community.mysql modules</span>
                </div>
                <div class="flow-arrow">➔ Grants ivolveuser ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Verified DB</span>
                    <span class="node-title">ivolve Database</span>
                    <span class="node-sub">SHOW DATABASES ok</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create Encrypted Vault File</h5>
            <pre><code class="language-bash"># Create group_vars directory:
mkdir -p group_vars/all

# Create and encrypt the vault file:
ansible-vault create group_vars/all/vault.yml</code></pre>
            <p>Define the database password inside the encrypted file:</p>
            <pre><code class="language-yaml">vault_mysql_password: "SuperSecretPassword123!"</code></pre>

            <h5>2. Author the MySQL Role (<code>roles/mysql/tasks/main.yml</code>)</h5>
            <pre><code class="language-yaml">---
- name: install mysql server and pymysql (for the mysql modules)
  ansible.builtin.apt:
    name:
      - mysql-server
      - python3-pymysql
    state: present
    update_cache: true

- name: start mysql (no systemd in the lab container)
  ansible.builtin.command: service mysql start
  changed_when: false

- name: create the ivolve database
  community.mysql.mysql_db:
    name: ivolve
    state: present
    login_unix_socket: /var/run/mysqld/mysqld.sock

- name: create ivolveuser with all privileges on ivolve
  community.mysql.mysql_user:
    name: ivolveuser
    host: "%"
    password: "{{ vault_mysql_password }}"
    priv: "ivolve.*:ALL"
    state: present
    login_unix_socket: /var/run/mysqld/mysqld.sock

- name: validate - connect as ivolveuser and list databases
  community.mysql.mysql_info:
    login_user: ivolveuser
    login_password: "{{ vault_mysql_password }}"
    login_host: 127.0.0.1
    filter: databases
  register: dbcheck
  changed_when: false

- name: show validation result
  ansible.builtin.debug:
    msg: "databases visible to ivolveuser: {{ dbcheck.databases | list }}"</code></pre>

            <h5>3. Playbook Configuration (<code>site.yml</code>)</h5>
            <pre><code class="language-yaml">---
- hosts: all
  become: true
  vars_files:
    - group_vars/all/vault.yml
  roles:
    - mysql</code></pre>

            <h5>4. Execute Playbook with Vault Credentials</h5>
            <pre><code class="language-bash"># Run playbook supplying vault password file:
#   --vault-password-file : Path to file containing decryption key
ansible-playbook -i inventory site.yml --vault-password-file .vault-pass</code></pre>

            <h5>5. Verify Connectivity as the New User</h5>
            <pre><code class="language-bash"># Connect directly using ivolveuser credentials:
mysql -u ivolveuser -p -h 127.0.0.1 -e "SHOW DATABASES;"</code></pre>
            <div class="terminal-output">
Database
information_schema
ivolve
performance_schema
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Python MySQL Dependency:</strong> The <code>community.mysql.mysql_db</code> and <code>mysql_user</code> modules require <code>python3-pymysql</code> to be installed on the managed target node to interact directly with MySQL sockets.</li>
                <li><strong>Vault Password Protection:</strong> Never commit the <code>.vault-pass</code> file to Git. Add <code>.vault-pass</code> to your <code>.gitignore</code> and restrict file permissions with <code>chmod 600 .vault-pass</code>.</li>
            </ul>
        """
    },
    {
        "id": "lab-28",
        "number": "Lab 28",
        "title": "Automated Host Discovery with AWS EC2 Dynamic Inventory",
        "module": "Ansible",
        "icon": "☁️",
        "tags": ["Dynamic Inventory", "AWS EC2", "amazon.aws", "Cloud Automation"],
        "summary": "Implement cloud-native host discovery using the amazon.aws.aws_ec2 dynamic inventory plugin to manage AWS EC2 instances filtered by tags.",
        "files": [
            ("Ansible/Lab28/README.md", "Dynamic inventory setup, AWS configuration, and run output"),
            ("Ansible/Lab28/aws_ec2.yml", "AWS EC2 dynamic inventory plugin configuration"),
            ("Ansible/Lab28/ec2.yml", "Playbook executing against dynamically discovered EC2 hosts"),
            ("Ansible/Lab28/group_vars/all.yml", "Connection variables for discovered cloud instances")
        ],
        "question": [
            "Configure AWS dynamic inventory using amazon.aws.aws_ec2 plugin.",
            "Filter instances dynamically tagged Server=ivolve.",
            "Execute Ansible ad-hoc commands and playbooks against dynamically discovered cloud instances.",
            "Terminate cloud instances cleanly after verification."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>In cloud environments, servers launch, terminate, and change IP addresses dynamically (e.g. Auto Scaling groups). Static inventory files quickly become outdated:</p>
            <ul>
                <li><strong>Dynamic Inventory Plugins:</strong> Query provider APIs (like AWS EC2) at runtime to discover active servers, public IPs, and metadata automatically.</li>
                <li><strong>Tag-Based Targeting:</strong> Instead of hardcoding IPs, playbooks target instances based on AWS tags (e.g. <code>tag:Server: ivolve</code>).</li>
                <li><strong>Ephemeral Automation:</strong> Newly launched instances join the inventory and receive configurations without modifying any inventory files.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Plugin</span>
                    <span class="node-title">aws_ec2.yml</span>
                    <span class="node-sub">amazon.aws plugin</span>
                </div>
                <div class="flow-arrow">➔ AWS API Call ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">AWS Cloud</span>
                    <span class="node-title">Tag: Server=ivolve</span>
                    <span class="node-sub">Discovers Running IPs</span>
                </div>
                <div class="flow-arrow">➔ Dynamic Inventory ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Playbook Run</span>
                    <span class="node-title">ec2.yml</span>
                    <span class="node-sub">Docker Installed on Cloud</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Prerequisites: AWS SDK and Ansible Collection</h5>
            <pre><code class="language-bash"># Install Python AWS SDK:
pip install boto3 botocore

# Install official Ansible AWS collection:
ansible-galaxy collection install amazon.aws</code></pre>

            <h5>2. Launch EC2 Instance with Target Tag</h5>
            <pre><code class="language-bash"># Launch Amazon Linux 2023 instance tagged Server=ivolve:
# (Ensure security group allows port 22 SSH from your IP)
aws ec2 run-instances \
  --image-id ami-0084a47cc718c111a \
  --count 1 \
  --instance-type t3.micro \
  --key-name nti-devops-key \
  --security-group-ids sg-0eae4711e8c34c6eb \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Server,Value=ivolve}]'</code></pre>

            <h5>3. Configure Dynamic Inventory (<code>aws_ec2.yml</code>)</h5>
            <p><em>Note:</em> The filename must end with <code>aws_ec2.yml</code> or <code>aws_ec2.yaml</code>.</p>
            <pre><code class="language-yaml">plugin: amazon.aws.aws_ec2
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
  ansible_python_interpreter: /usr/bin/python3</code></pre>

            <h5>4. Query Live Cloud Inventory</h5>
            <pre><code class="language-bash"># Test discovery graph from AWS API:
#   --graph : Outputs discovered host hierarchy
ansible-inventory -i aws_ec2.yml --graph</code></pre>
            <div class="terminal-output">
@all:
  |--@ungrouped:
  |--@aws_ec2:
  |  |--3.75.247.89
            </div>

            <h5>5. Execute Playbook Against Discovered Cloud Instances (<code>ec2.yml</code>)</h5>
            <pre><code class="language-yaml">---
- hosts: all
  become: true
  tasks:
    - name: install docker
      ansible.builtin.dnf:
        name: docker
        state: present

    - name: start and enable docker
      ansible.builtin.service:
        name: docker
        state: started
        enabled: true

    - name: docker version
      ansible.builtin.command: docker --version
      register: dv
      changed_when: false

    - name: show result
      ansible.builtin.debug:
        msg: "{{ ansible_hostname }} -> {{ dv.stdout }}"</code></pre>
            <pre><code class="language-bash"># Run playbook against discovered instances:
ansible-playbook -i aws_ec2.yml ec2.yml</code></pre>
            <div class="terminal-output">
ok: [3.75.247.89] => {
    "msg": "ip-172-31-21-200 -> Docker version 25.0.14, build 0bab007"
}
PLAY RECAP *********************************************************************
3.75.247.89                : ok=5    changed=2    unreachable=0    failed=0
            </div>

            <h5>6. Terminate Cloud Resources</h5>
            <pre><code class="language-bash"># Clean up EC2 instance:
aws ec2 terminate-instances --instance-ids &lt;INSTANCE_ID&gt;</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Naming Requirement:</strong> The inventory configuration file must end in <code>aws_ec2.yml</code> or <code>aws_ec2.yaml</code>. Ansible uses the filename pattern to identify and invoke the dynamic inventory plugin.</li>
                <li><strong>Connection Variables:</strong> In plugin inventories, define connection variables (like <code>ansible_user</code> and private key path) directly within the plugin's <code>vars:</code> block so they reliably attach to dynamically discovered hosts.</li>
            </ul>
        """
    }
]

