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
            <p>Playbooks are YAML files describing the state target servers should be in. Each play defines target hosts (<code>hosts: all</code>), privilege escalation (<code>become: true</code>), and an ordered list of tasks:</p>
            <ul>
                <li><strong>Idempotency:</strong> Tasks only make changes if the system isn't already in the desired state. If <code>docker.io</code> is already installed, Ansible reports <code>ok</code> instead of <code>changed</code>. A clean second run always returns <code>changed=0</code>.</li>
                <li><strong>Keyring Management:</strong> Modern Debian and Ubuntu deprecated <code>apt-key add</code>. Third-party repository keys must now be converted to binary format and saved under <code>/usr/share/keyrings/</code>, referenced with <code>signed-by</code> in the repo definition.</li>
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
# Target all hosts listed in inventory
- hosts: all
  # Sudo escalation so tasks can install system packages and write /usr/local/bin
  become: true
  # Collect host architecture, OS distribution, and network facts for module use
  gather_facts: true

  tasks:
    # --- TASK 1: DOCKER RUNTIME ---
    - name: install docker
      ansible.builtin.apt:
        # Standard Ubuntu/Debian Docker runtime and CLI package
        name: docker.io
        # Idempotent state: installs if missing, skips if already present
        state: present
        # Runs apt-get update first so fresh containers don't fail on missing indices
        update_cache: true

    # --- TASK 2: JENKINS DEPENDENCIES ---
    - name: install java and gnupg (jenkins dependencies)
      ansible.builtin.apt:
        name:
          # Jenkins 2.x requires Java 17+ (headless avoids pulling 300MB of GUI/X11 libraries)
          - openjdk-17-jre-headless
          # Needed for gpg binary to dearmor repository keys into binary format
          - gnupg
        # Ensures both packages are installed; skips if already satisfied
        state: present

    # --- TASK 3: JENKINS GPG REPOSITORY KEY ---
    # Fetch 2026 key — the historical 2023 key expired in March 2026 and causes apt NO_PUBKEY errors
    - name: add jenkins repository key
      ansible.builtin.get_url:
        # Official Jenkins stable signing key URL
        url: https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
        # Destination file for ASCII-armored key
        dest: /usr/share/keyrings/jenkins-keyring.asc
        # Standard read permissions for root and apt service accounts
        mode: "0644"
        # Overwrite destination file to replace expired keys
        force: true

    # --- TASK 4: DEARMOR KEYRING TO BINARY ---
    # APT signed-by expects binary OpenPGP (.gpg), not ASCII-armored (.asc)
    - name: dearmor the jenkins key
      # gpg --dearmor converts ASCII armor to binary; --yes overwrites without prompting
      ansible.builtin.command: "gpg --dearmor --yes -o /usr/share/keyrings/jenkins-keyring.gpg /usr/share/keyrings/jenkins-keyring.asc"
      args:
        # Idempotency guard: skips execution if binary file already exists (returns changed=0)
        creates: /usr/share/keyrings/jenkins-keyring.gpg

    # --- TASK 5: JENKINS APT REPOSITORY ---
    - name: add jenkins repository
      ansible.builtin.apt_repository:
        # signed-by restricts key trust exclusively to this repository, preventing apt-key poisoning
        repo: "deb [signed-by=/usr/share/keyrings/jenkins-keyring.gpg] https://pkg.jenkins.io/debian-stable binary/"
        # Adds repository entry if not already present
        state: present
        # Writes entry to /etc/apt/sources.list.d/jenkins.list instead of main sources.list
        filename: jenkins

    # --- TASK 6: JENKINS SERVER PACKAGE ---
    - name: install jenkins
      ansible.builtin.apt:
        # Package pulled from the newly registered Jenkins APT repository
        name: jenkins
        # Installs package and registers systemd/init service
        state: present

    # --- TASK 7: STANDALONE KUBECTL BINARY ---
    # Fetch standalone binary directly into PATH, avoiding the overhead of the Google cloud apt repo
    - name: install kubectl
      ansible.builtin.get_url:
        # Official Kubernetes release binary URL for amd64 Linux
        url: https://dl.k8s.io/release/v1.33.13/bin/linux/amd64/kubectl
        # Placed directly in system executable directory accessible by all users
        dest: /usr/local/bin/kubectl
        # rwxr-xr-x: grants execute permissions so non-root users can run kubectl
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
            <p>When a single playbook grows, splitting it into <strong>Roles</strong> keeps tasks organized by tool. Each role lives in its own directory (e.g. <code>roles/docker/tasks/main.yml</code>). The master playbook simply declares which roles to run on which hosts, executing them in listed order.</p>
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
    # Standard Ubuntu/Debian Docker runtime package
    name: docker.io
    # Idempotent state: installs if missing, skips if already present
    state: present
    # Refreshes package cache before installing so lookups don't fail
    update_cache: true</code></pre>

            <p><strong><code>roles/kubectl/tasks/main.yml</code>:</strong></p>
            <pre><code class="language-yaml">---
# Download standalone binary directly into PATH, avoiding apt repo overhead
- name: install kubectl
  ansible.builtin.get_url:
    # Official v1.33.13 Linux amd64 binary URL
    url: https://dl.k8s.io/release/v1.33.13/bin/linux/amd64/kubectl
    # Target directory in standard system $PATH
    dest: /usr/local/bin/kubectl
    # rwxr-xr-x permissions allowing all users to execute kubectl
    mode: "0755"</code></pre>

            <p><strong><code>roles/jenkins/tasks/main.yml</code>:</strong></p>
            <pre><code class="language-yaml">---
# Prerequisites: Headless Java 17 runtime for Jenkins + gnupg for key conversion
- name: install java and gnupg
  ansible.builtin.apt:
    name:
      - openjdk-17-jre-headless  # Java runtime without GUI overhead
      - gnupg                    # Provides gpg binary for dearmoring
    state: present

# Download official signing key (2026 key; 2023 key expired in March 2026)
- name: add jenkins repository key
  ansible.builtin.get_url:
    url: https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
    dest: /usr/share/keyrings/jenkins-keyring.asc
    mode: "0644"   # Standard read permissions for apt
    force: true    # Overwrite if key exists to ensure it's up to date

# Convert ASCII key to binary format required by Debian signed-by
- name: dearmor the jenkins key
  ansible.builtin.command: "gpg --dearmor --yes -o /usr/share/keyrings/jenkins-keyring.gpg /usr/share/keyrings/jenkins-keyring.asc"
  args:
    # Idempotency guard: skips running gpg if binary keyring already exists
    creates: /usr/share/keyrings/jenkins-keyring.gpg

# Register repository with scoped key verification
- name: add jenkins repository
  ansible.builtin.apt_repository:
    # signed-by limits key trust strictly to this repository URL
    repo: "deb [signed-by=/usr/share/keyrings/jenkins-keyring.gpg] https://pkg.jenkins.io/debian-stable binary/"
    state: present
    # Writes to /etc/apt/sources.list.d/jenkins.list
    filename: jenkins

- name: install jenkins
  ansible.builtin.apt:
    name: jenkins   # Package from newly added Jenkins apt source
    state: present  # Installs package and registers systemd service</code></pre>

            <h5>3. Master Orchestration Playbook (<code>site.yml</code>)</h5>
            <pre><code class="language-yaml">---
# Master playbook orchestrating modular roles
- hosts: all
  # Sudo escalation so roles can install packages and write /usr/local/bin
  become: true
  roles:
    # Executed sequentially from top to bottom:
    - docker   # Role 1: Installs docker container runtime
    - kubectl  # Role 2: Installs kubectl client binary
    - jenkins  # Role 3: Installs Java 17, Jenkins apt repo, and server</code></pre>

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
            <p>Storing plaintext passwords in Git is a security risk. <strong>Ansible Vault</strong> encrypts variable files at rest using AES-256. The encrypted file is safe to commit; only runners with the password file (<code>--vault-password-file</code>) can decrypt the values in memory during playbook execution.</p>
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
            <pre><code class="language-yaml"># AES-256 encrypted string created with ansible-vault
# Decrypted in memory at runtime via --vault-password-file; never written plaintext to disk
vault_mysql_password: "SuperSecretPassword123!"</code></pre>

            <h5>2. Author the MySQL Role (<code>roles/mysql/tasks/main.yml</code>)</h5>
            <pre><code class="language-yaml">---
# python3-pymysql is required on the target node so Ansible community.mysql modules can run
- name: install mysql server and pymysql
  ansible.builtin.apt:
    name:
      - mysql-server     # MySQL database server daemon
      - python3-pymysql  # Python MySQL driver required by community.mysql modules
    state: present
    update_cache: true   # Refresh package index before installation

# Sysvinit service start: needed because Docker lab containers don't run systemd PID 1
- name: start mysql
  ansible.builtin.command: service mysql start
  # changed_when: false prevents marking this task as changed on every run (preserves idempotency)
  changed_when: false

# Creates schema; connects locally as root via Unix socket without password
- name: create the ivolve database
  community.mysql.mysql_db:
    name: ivolve
    state: present       # Idempotent: creates database only if it does not exist
    login_unix_socket: /var/run/mysqld/mysqld.sock  # Auth socket authentication for local root

# Provisions database user with credentials resolved from Ansible Vault
- name: create ivolveuser with all privileges on ivolve
  community.mysql.mysql_user:
    name: ivolveuser
    host: "%"            # Wildcard host: allows connections from any IP/container
    password: "{{ vault_mysql_password }}"  # Variable decrypted in-memory from group_vars/all/vault.yml
    priv: "ivolve.*:ALL" # Restricts full permissions strictly to ivolve database tables
    state: present       # Idempotent: creates user or updates password if changed
    login_unix_socket: /var/run/mysqld/mysqld.sock

# Verification task: connects as the newly created user using the vault password
- name: validate - connect as ivolveuser and list databases
  community.mysql.mysql_info:
    login_user: ivolveuser
    login_password: "{{ vault_mysql_password }}"
    login_host: 127.0.0.1  # TCP loopback connection to test remote grant
    filter: databases      # Restricts query to database list
  register: dbcheck        # Captures module output dictionary into variable
  changed_when: false      # Read-only query; never alters database state

# Print visible databases to confirm user grants are working
- name: show validation result
  ansible.builtin.debug:
    msg: "databases visible to ivolveuser: {{ dbcheck.databases | list }}"</code></pre>

            <h5>3. Playbook Configuration (<code>site.yml</code>)</h5>
            <pre><code class="language-yaml">---
- hosts: all
  become: true
  vars_files:
    # Loads AES-256 encrypted variables into playbook scope
    - group_vars/all/vault.yml
  roles:
    # Runs MySQL provisioning role with vault variables available
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
            <p>In cloud environments, static IP inventories don't scale because servers launch, stop, or change IPs dynamically. <strong>Dynamic Inventory plugins</strong> (like <code>amazon.aws.aws_ec2</code>) query the AWS API at runtime, discover active instances matching specific tags (e.g. <code>Server=ivolve</code>), and hand their public IPs directly to Ansible.</p>
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
            <pre><code class="language-yaml"># AWS EC2 dynamic inventory configuration. Filename must end with aws_ec2.yml or aws_ec2.yaml.
plugin: amazon.aws.aws_ec2
regions:
  # AWS region where target EC2 instances are provisioned
  - eu-central-1
filters:
  # Filter: only discover instances tagged Server=ivolve, ignoring other VPC workloads
  tag:Server: ivolve
  # Filter: only target active, running instances (ignores stopped/terminated nodes)
  instance-state-name: running
hostnames:
  # Use public IPv4 address as inventory_hostname so Ansible dials over SSH
  - ip-address
vars:
  # Default SSH username for Amazon Linux 2023 AMIs
  ansible_user: ec2-user
  # SSH private key matching the AWS Key Pair used at launch
  ansible_ssh_private_key_file: /root/.ssh/nti-devops-key.pem
  # Explicit Python 3 interpreter path on Amazon Linux 2023
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
# Play targets all dynamically discovered EC2 instances from aws_ec2.yml
- hosts: all
  # Sudo escalation so dnf and systemd commands can run as root
  become: true
  tasks:
    # Amazon Linux 2023 uses dnf instead of yum or apt
    - name: install docker
      ansible.builtin.dnf:
        name: docker     # Official Docker package in Amazon Linux 2023 repos
        state: present   # Idempotent: ensures package is installed

    # Service configuration via systemd
    - name: start and enable docker
      ansible.builtin.service:
        name: docker     # Docker systemd service unit
        state: started   # Ensures daemon is running (starts if stopped)
        enabled: true    # Configures systemd to start Docker on system reboot

    # Verification: check installed Docker version on cloud instance
    - name: docker version
      ansible.builtin.command: docker --version
      register: dv         # Captures command stdout, stderr, and return code
      changed_when: false  # Read-only check: skips marking task as changed

    # Print output with hostname to confirm successful execution across cloud nodes
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

