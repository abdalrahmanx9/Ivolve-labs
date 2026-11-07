# generator/module3_kubernetes.py

LABS_MODULE_3 = [
    {
        "id": "lab-9",
        "number": "Lab 09",
        "title": "Deploy Kubernetes Cluster using Kubeadm",
        "module": "Kubernetes",
        "icon": "☸️",
        "tags": ["kubeadm", "containerd", "Calico CNI", "Cluster Architecture"],
        "summary": "Build a real multi-node Kubernetes cluster from scratch using containerd and Calico networking instead of a pre-packaged simulator.",
        "question": [
            "Install and configure containerd as the container runtime on all nodes.",
            "Install kubeadm, kubelet, and kubectl on the control plane and worker nodes.",
            "Configure kubectl to communicate with the Kubernetes cluster.",
            "Install the Calico CNI plugin to enable pod networking across the cluster.",
            "Initialize the control plane node using kubeadm init.",
            "Join the worker nodes to the cluster using the kubeadm join command.",
            "Verify that all nodes are in the Ready state and that the cluster components are running correctly."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Docker alone only runs containers on a single computer. But what happens if that computer's power goes out or crashes? Your entire company website goes down.</p>
            <p><strong>Kubernetes</strong> groups multiple computers together into a single cluster so they act like one giant supercomputer:</p>
            <ul>
                <li><strong>The Boss (Control Plane / Master Node):</strong> Doesn't run your apps. Instead, it decides which computer has enough free memory, keeps track of cluster health, and automatically replaces dead containers.
                    <br>&bull; <code>kube-apiserver</code>: The front desk receptionist. Every command you run with <code>kubectl</code> talks to this server.
                    <br>&bull; <code>etcd</code>: The database storing cluster state.</li>
                <li><strong>The Workers (Worker Nodes):</strong> The computers where your application containers (Pods) actually run.
                    <br>&bull; <code>kubelet</code>: The foreman on each worker node that receives orders from the Boss and starts containers using <code>containerd</code>.</li>
                <li><strong>Why do we need Calico CNI?</strong> By default, Kubernetes nodes cannot route traffic between pods on different servers. <strong>Calico</strong> acts like an internal private highway (overlay network) giving every pod its own IP address across the entire cluster.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Master Node</span>
                    <span class="node-title">Control Plane</span>
                    <span class="node-sub">kubeadm init</span>
                </div>
                <div class="flow-arrow">➔ Join Token ➔</div>
                <div class="flow-node">
                    <span class="node-step">Worker Node</span>
                    <span class="node-title">kubelet + containerd</span>
                    <span class="node-sub">kubeadm join</span>
                </div>
                <div class="flow-arrow">➔ CNI Overlay ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Networking</span>
                    <span class="node-title">Project Calico</span>
                    <span class="node-sub">192.168.0.0/16</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node success">
                    <span class="node-step">Cluster Status</span>
                    <span class="node-title">Nodes Ready</span>
                    <span class="node-sub">0% Packet Loss Ping</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands (Official Kubernetes & Calico Documentation)</h4>

            <div class="official-doc-callout" style="background: rgba(14, 165, 233, 0.08); border-left: 4px solid var(--accent-cyan); padding: 12px 16px; border-radius: 6px; margin-bottom: 20px;">
                <p style="margin: 0 0 6px 0; font-weight: 600;">📖 Official Documentation Standards Followed:</p>
                <ul style="margin: 0; padding-left: 20px; font-size: 0.9em;">
                    <li><strong>Kubernetes Official Docs:</strong> <a href="https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/" target="_blank" rel="noopener">Installing kubeadm</a> &amp; <a href="https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd" target="_blank" rel="noopener">Container Runtimes (containerd)</a></li>
                    <li><strong>Project Calico Official Docs:</strong> <a href="https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart" target="_blank" rel="noopener">Calico Quickstart for Kubernetes</a></li>
                </ul>
            </div>

            <h5>1. System Prerequisites (Run on Both Nodes - kubernetes.io)</h5>
            <p>According to official Kubernetes documentation, swap memory must be disabled and Linux kernel networking modules must be loaded with packet filtering enabled:</p>
            <pre><code class="language-bash"># Disable swap memory (Kubernetes scheduler requires predictable memory allocations):
#   -a : Turns off all swap devices and files
sudo swapoff -a

# Persist swap disablement across system reboots in filesystem table:
#   -i : Edits /etc/fstab in-place
sudo sed -i '/ swap / s/^\\(.*\\)$/#\\1/g' /etc/fstab

# Load required Linux networking kernel modules (overlay & br_netfilter):
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Enable Linux kernel packet forwarding and bridged IPv4 traffic to iptables:
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# Apply sysctl parameters immediately without rebooting:
#   --system : Loads settings from all system configuration directories
sudo sysctl --system</code></pre>

            <h5>2. Install and Configure containerd Runtime (Both Nodes - kubernetes.io)</h5>
            <p>Install containerd and configure the <code>systemd</code> cgroup driver as mandated by the Kubernetes production container runtime documentation:</p>
            <pre><code class="language-bash"># Install containerd container runtime package:
#   -y : Automatically confirm installation
sudo apt-get update && sudo apt-get install -y containerd

# Generate official default containerd configuration:
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Configure systemd cgroup driver (mandatory for kubelet stability according to kubernetes.io):
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml

# Restart and enable containerd service:
sudo systemctl restart containerd
sudo systemctl enable containerd</code></pre>

            <h5>3. Install kubelet, kubeadm, and kubectl (Both Nodes - pkgs.k8s.io)</h5>
            <p>Install Kubernetes tools from the official community repository (<code>pkgs.k8s.io</code>):</p>
            <pre><code class="language-bash"># Install apt HTTPS transport packages and download Kubernetes official signing key:
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# Create keyrings directory if not present:
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor --yes -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add official Kubernetes apt repository:
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Install Kubernetes cluster tools and lock package versions to prevent accidental drift:
#   apt-mark hold : Locks installed version against automatic apt upgrade
sudo apt-get update && sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Enable kubelet daemon service:
sudo systemctl enable --now kubelet</code></pre>

            <h5>4. Initialize the Master Node (Control Plane - kubernetes.io)</h5>
            <p>Initialize the control plane with the standard pod network CIDR recommended by Calico (<code>192.168.0.0/16</code>):</p>
            <pre><code class="language-bash"># Bootstrap control plane with Pod CIDR matching Calico:
#   --pod-network-cidr=192.168.0.0/16 : Standard Calico default subnet block for Pod IP pool
sudo kubeadm init --pod-network-cidr=192.168.0.0/16

# Configure kubeconfig authentication credentials for your regular non-root user:
#   mkdir -p           : Creates ~/.kube directory if not existing
#   cp -i              : Prompts before overwriting existing config
#   $(id -u):$(id -g)  : Sets ownership to current user UID and GID
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config</code></pre>

            <h5>5. Install Calico CNI Networking (docs.tigera.io)</h5>
            <p>According to official Project Calico documentation, deploy Calico using the Tigera Operator:</p>
            <pre><code class="language-bash"># Step 5a: Install the Tigera Calico operator and CRDs:
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/tigera-operator.yaml

# Step 5b: Install Calico custom resources (configures Calico to manage the 192.168.0.0/16 pool):
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/custom-resources.yaml

# (Alternative from Calico Docs): If you prefer single-manifest deployment without operator:
# kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/calico.yaml

# Monitor Calico pods until all report Running status:
#   -n calico-system : Namespace where Tigera Operator provisions Calico pods
#   -w / --watch     : Streams pod status transitions live
kubectl get pods -n calico-system -w</code></pre>

            <h5>6. Join Worker Node to the Cluster</h5>
            <p>Run the join command printed by <code>kubeadm init</code> on your worker node:</p>
            <pre><code class="language-bash"># Attach worker node to control plane:
#   &lt;MASTER_IP&gt;:6443              : Control plane API server endpoint
#   --token &lt;TOKEN&gt;               : Cluster bootstrap authorization token
#   --discovery-token-ca-cert-hash: SHA256 hash validating control plane Root CA
sudo kubeadm join &lt;MASTER_IP&gt;:6443 --token &lt;TOKEN&gt; \
  --discovery-token-ca-cert-hash sha256:&lt;HASH&gt;</code></pre>

            <h5>7. Verify Cluster Status</h5>
            <pre><code class="language-bash"># Check node readiness and extended details across cluster:
#   -o wide : Displays node internal IP, OS image, kernel version, and container runtime
kubectl get nodes -o wide
# Output shows all nodes in Ready state!

# List pods across all namespaces:
#   -A / --all-namespaces : Queries pods across every namespace in the cluster
kubectl get pods -A
# All Calico, CoreDNS, etcd, and kube-apiserver pods show Running!</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Why Must Swap Be Off?</strong> The Kubernetes scheduler assumes 100% predictable memory performance. If Linux starts swapping memory to a slow hard drive, pods become unresponsive and the scheduler miscalculates available capacity. That is why <code>swapoff</code> is mandatory.</li>
                <li><strong>Forgot the Join Token?</strong> If your join token expires after 24 hours, generate a fresh join command on the master node anytime with:
                    <br><code>kubeadm token create --print-join-command</code></li>
            </ul>
        """
    },
    {
        "id": "lab-10",
        "number": "Lab 10",
        "title": "Node Isolation Using Taints and Labels in Kubernetes",
        "module": "Kubernetes",
        "icon": "🏷️",
        "tags": ["Taints & Tolerations", "Node Labels", "NodeSelector", "Targeted Scheduling"],
        "summary": "Reserve specific worker nodes for dedicated projects by repelling unwanted pods with Taints and attracting target pods with Labels.",
        "question": [
            "Apply a taint to a worker node with key workload, value ivolveApp, and effect NoSchedule to prevent pods from being scheduled on the node unless they have a matching toleration.",
            "Label the same worker node with project=ivolve to identify it for targeted pod scheduling.",
            "Verify that the taint and label have been applied correctly using kubectl describe node and kubectl get nodes --show-labels."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Imagine your company has 10 general servers and 1 expensive server with high-speed SSDs dedicated to Project iVolve. If developers start launching test apps, Kubernetes might blindly put random test pods on your expensive server, wasting its capacity.</p>
            <p>We use a two-part lock-and-key system to solve this:</p>
            <ul>
                <li><strong>Part 1: The Taint (The Repellent / Keep Out Sign):</strong> You put a taint (<code>workload=ivolveApp:NoSchedule</code>) on the node. Now, the Kubernetes scheduler will <strong>refuse</strong> to put any pod on that node. Pods are repelled.</li>
                <li><strong>Part 2: The Toleration (The VIP Pass):</strong> You give your project pods a special VIP pass called a <strong>Toleration</strong>. Now they are permitted to land on the tainted node.</li>
                <li><strong>Part 3: The Label & NodeSelector (The Target Magnet):</strong> A toleration only means <em>"I am allowed here"</em>—it does not force the pod to go there. Adding <code>project=ivolve</code> on the node and <code>nodeSelector: project: ivolve</code> on the pod actively guides the pod to that specific machine.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-comparison">
                <div class="comparison-card">
                    <div class="comp-badge danger">blocked-pod</div>
                    <div class="comp-flow">No Toleration ➔ Hits Tainted Node ➔ REPELLED!</div>
                    <div class="comp-metric danger">Sent to other workers</div>
                    <div class="comp-note">Cannot land on desktop-worker because it lacks the VIP pass.</div>
                </div>
                <div class="comparison-card">
                    <div class="comp-badge success">allowed-pod</div>
                    <div class="comp-flow">Toleration + Label ➔ Hits Node ➔ ACCEPTED!</div>
                    <div class="comp-metric success">Lands on desktop-worker</div>
                    <div class="comp-note">Matches taint toleration and project=ivolve label selector.</div>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Apply Taint and Label to the Worker Node</h5>
            <pre><code class="language-bash"># Apply taint to repel general pods from the worker node:
#   node desktop-worker          : Target node to apply the taint to
#   workload=ivolveApp:NoSchedule: Key=workload, Value=ivolveApp, Effect=NoSchedule
#                                  (NoSchedule prevents pods without matching toleration from scheduling)
kubectl taint node desktop-worker workload=ivolveApp:NoSchedule

# Apply label so project pods can specifically target it using nodeSelector:
#   project=ivolve : Key=value label attached to node metadata
kubectl label node desktop-worker project=ivolve</code></pre>

            <h5>2. Verify Node Configuration</h5>
            <pre><code class="language-bash"># Check taint status on target node:
#   describe node &lt;name&gt; : Prints detailed node specification, capacity, and conditions
#   grep -A1 Taints      : -A1 prints matching line plus 1 line of trailing context
kubectl describe node desktop-worker | grep -A1 Taints
# Output: Taints: workload=ivolveApp:NoSchedule

# Check node labels:
#   --show-labels        : Appends LABELS column to node listing output
kubectl get nodes --show-labels | grep project=ivolve
# Shows desktop-worker with label project=ivolve</code></pre>

            <h5>3. Deploy the Authorized Pod (<code>allowed-pod.yaml</code>)</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab10/allowed-pod.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab10/allowed-pod.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: Pod
metadata:
  name: allowed-pod
spec:
  nodeSelector:
    project: ivolve                    # Attracts pod to this node
  tolerations:
    - key: "workload"                  # The VIP pass allowing it past the taint
      operator: "Equal"
      value: "ivolveApp"
      effect: "NoSchedule"
  containers:
    - name: nginx
      image: nginx:alpine</code></pre>

            <h5>4. Deploy the Blocked Pod (<code>blocked-pod.yaml</code>)</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab10/blocked-pod.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab10/blocked-pod.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: Pod
metadata:
  name: blocked-pod
spec:
  containers:
    - name: nginx
      image: nginx:alpine</code></pre>

            <h5>5. Proof of Isolation</h5>
            <pre><code class="language-bash"># Apply both pod manifests simultaneously:
#   -f allowed-pod.yaml -f blocked-pod.yaml : Pass multiple manifest files in a single execution
kubectl apply -f allowed-pod.yaml -f blocked-pod.yaml

# Check pod scheduling distribution:
#   -o custom-columns : Custom table output selecting specific JSONPath fields
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName</code></pre>
            <div class="terminal-output">
NAME          STATUS    NODE
allowed-pod   Running   desktop-worker    <- Allowed onto isolated node!
blocked-pod   Running   desktop-worker2   <- Repelled by taint, scheduled elsewhere!
            </div>
            <pre><code class="language-bash">kubectl delete pod allowed-pod blocked-pod</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Removing a Taint:</strong> If you ever make a mistake and want to delete a taint from a node, put a minus sign (<code>-</code>) at the end of the command:
                    <br><code>kubectl taint node desktop-worker workload=ivolveApp:NoSchedule-</code></li>
                <li><strong>NoSchedule vs NoExecute:</strong> <code>NoSchedule</code> only prevents <em>new</em> pods from landing. If pods are already running on the node when you add the taint, they stay there. If you use <code>NoExecute</code>, Kubernetes kicks off existing pods immediately!</li>
            </ul>
        """
    },
    {
        "id": "lab-11",
        "number": "Lab 11",
        "title": "Namespace Management and Resource Quota Enforcement",
        "module": "Kubernetes",
        "icon": "📦",
        "tags": ["Namespaces", "ResourceQuota", "Multi-Tenancy", "RFC 1123"],
        "summary": "Create isolated team environments using Namespaces and enforce strict boundaries with ResourceQuotas to prevent cluster overload.",
        "question": [
            "Create a Kubernetes namespace named ivolve to isolate application resources.",
            "Create a ResourceQuota named ivolveQuota in the ivolve namespace to limit the total number of pods to 3.",
            "Verify that the ResourceQuota is applied correctly and confirm that Kubernetes prevents the creation of additional pods when the limit is reached."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Imagine your company has two developer teams sharing one Kubernetes cluster: Team Alpha and Team Beta.</p>
            <ul>
                <li><strong>What is a Namespace?</strong> Think of a Namespace like an apartment inside an apartment building. Team Alpha gets apartment <code>alpha</code>, and Team Beta gets apartment <code>beta</code>. They can both name a pod <code>web-server</code> and they will never collide because they live in separate rooms.</li>
                <li><strong>What is a ResourceQuota?</strong> What if someone on Team Alpha accidentally runs an infinite loop that creates 10,000 pods and crashes the entire server, taking down Team Beta too?
                    <br>&bull; A <strong>ResourceQuota</strong> sets a strict ceiling on the apartment. In this lab, we set a hard cap of <strong>3 pods maximum</strong>. If Team Alpha tries to create a 4th pod, Kubernetes rejects it with an immediate error.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Setup</span>
                    <span class="node-title">Namespace: ivolve</span>
                    <span class="node-sub">Logical Isolation</span>
                </div>
                <div class="flow-arrow">➔ Apply ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">ResourceQuota</span>
                    <span class="node-title">Limit: pods = "3"</span>
                    <span class="node-sub">ivolve-quota</span>
                </div>
                <div class="flow-arrow">➔ 4th Pod Attempt ➔</div>
                <div class="flow-node danger">
                    <span class="node-step">Rejected</span>
                    <span class="node-title">403 Forbidden</span>
                    <span class="node-sub">exceeded quota!</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create the Isolated Namespace</h5>
            <pre><code class="language-bash">kubectl create namespace ivolve</code></pre>

            <h5>2. Create the ResourceQuota Manifest</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab11/resourcequota.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab11/resourcequota.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: ResourceQuota
metadata:
  name: ivolve-quota                   # Must be lowercase (RFC 1123 standard)
  namespace: ivolve
spec:
  hard:
    pods: "3"                          # Hard limit: maximum 3 pods in this namespace</code></pre>

            <pre><code class="language-bash">kubectl apply -f resourcequota.yaml</code></pre>

            <h5>3. Test the Limit</h5>
            <p>Create 3 pods to fill up the quota:</p>
            <pre><code class="language-bash"># Create 3 pods to consume the allocated quota in namespace:
#   run &lt;name&gt;     : Imperatively creates a standalone Pod
#   --image=busybox: Lightweight Linux image
#   -n ivolve      : Target namespace subject to ivolve-quota
#   -- sleep 3600  : Overrides container command to keep pod running in background
kubectl run test-1 --image=busybox -n ivolve -- sleep 3600
kubectl run test-2 --image=busybox -n ivolve -- sleep 3600
kubectl run test-3 --image=busybox -n ivolve -- sleep 3600

# Inspect quota consumption and current utilization:
#   -n ivolve : Scope query to ivolve namespace
kubectl get resourcequota -n ivolve</code></pre>
            <div class="terminal-output">
NAME           AGE   REQUEST    LIMIT
ivolve-quota   30s   pods: 3    pods: 3   (100% Full)
            </div>

            <h5>4. Attempt to Create a 4th Pod (Quota Enforcement)</h5>
            <pre><code class="language-bash"># This command will be rejected by the API admission controller:
kubectl run test-4 --image=busybox -n ivolve -- sleep 3600</code></pre>
            <div class="terminal-output">
Error from server (Forbidden): pods "test-4" is forbidden: exceeded quota: ivolve-quota, requested: pods=1, used: pods=3, limited: pods=3
            </div>

            <pre><code class="language-bash"># Clean up test pods:
kubectl delete pod test-1 test-2 test-3 -n ivolve</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Naming Gotcha (RFC 1123):</strong> The lab sheet says <code>ivolveQuota</code>. In Kubernetes, resource names must always be lowercase alphanumeric characters or hyphens (<code>ivolve-quota</code>). If you write camelCase letters like <code>ivolveQuota</code>, Kubernetes rejects the YAML with a syntax error.</li>
            </ul>
        """
    },
    {
        "id": "lab-12",
        "number": "Lab 12",
        "title": "Managing Configuration and Sensitive Data with ConfigMaps and Secrets",
        "module": "Kubernetes",
        "icon": "🔐",
        "tags": ["ConfigMaps", "Secrets", "Base64", "Decoupled Config"],
        "summary": "Inject database URLs through ConfigMaps and store passwords safely inside Base64-encoded Kubernetes Secrets.",
        "question": [
            "Create a ConfigMap named ivolveCM in ivolve ns to store non-sensitive MySQL configuration variables:",
            "  • DB_HOST: The hostname of the MySQL StatefulSet's headless Service.",
            "  • DB_USER: The application database user authorized to connect to the ivolve database.",
            "Create a Secret named ivolveSecret in ivolve ns to store sensitive MySQL credentials:",
            "  • MYSQL_ROOT_PASSWORD: The root password for the MySQL database.",
            "  • DB_PASSWORD: The password for the application database user specified by DB_USER.",
            "Use Base64 encoding to encode the Secret data values when defining the Secret using a YAML manifest."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Never write passwords or database hostnames directly inside your application code. Why? Because you would have to edit and recompile your code every time you switch from local testing to staging or production.</p>
            <p><strong>Kubernetes gives you two distinct storage boxes:</strong></p>
            <ul>
                <li><strong>Box 1: ConfigMap (For Non-Sensitive Info):</strong> Put public settings here: server hostnames, port numbers, log levels, and database usernames (e.g., <code>DB_USER: ivolve</code>).</li>
                <li><strong>Box 2: Secret (For Confidential Info):</strong> Put passwords, API tokens, and private SSH keys here. Secret values are encoded in <strong>Base64</strong> and stored in a special temporary memory filesystem inside pods so they are never written to unencrypted disks.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Public Config</span>
                    <span class="node-title">ConfigMap (ivolve-cm)</span>
                    <span class="node-sub">DB_HOST + DB_USER</span>
                </div>
                <div class="flow-arrow">➔ envFrom ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Injected at Runtime</span>
                    <span class="node-title">Application Pods</span>
                    <span class="node-sub">Namespace: ivolve</span>
                </div>
                <div class="flow-arrow">➔ envFrom ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Confidential</span>
                    <span class="node-title">Secret (ivolve-secret)</span>
                    <span class="node-sub">Base64 Encoded Passwords</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create the ConfigMap for Non-Sensitive Variables</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab12/configmap.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab12/configmap.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: ConfigMap
metadata:
  name: ivolve-cm
  namespace: ivolve
data:
  DB_HOST: "ivolve-db-svc.ivolve.svc.cluster.local"   # Headless service DNS from Lab 14
  DB_USER: "ivolve"</code></pre>
            <pre><code class="language-bash">kubectl apply -f configmap.yaml</code></pre>

            <h5>2. Encode Passwords and Create the Secret</h5>
            <p>Use the <code>base64</code> terminal command to encode the passwords:</p>
            <pre><code class="language-bash"># Encode passwords into Base64 format:
#   -n : Suppresses trailing newline (prevents appending hidden \n that breaks password authentication)
echo -n 'ivolveroot123' | base64    # -> aXZvbHZlcm9vdDEyMw==
echo -n 'ivolvedb123'   | base64    # -> aXZvbHZlZGIxMjM=</code></pre>

            <div class="file-links-bar">
                <a href="Kubernetes/Lab12/secret.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab12/secret.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: Secret
metadata:
  name: ivolve-secret
  namespace: ivolve
type: Opaque                           # Standard unformatted arbitrary user-defined secret data
data:
  MYSQL_ROOT_PASSWORD: "aXZvbHZlcm9vdDEyMw=="
  DB_PASSWORD: "aXZvbHZlZGIxMjM="</code></pre>
            <pre><code class="language-bash">kubectl apply -f secret.yaml</code></pre>

            <h5>3. Verify Objects and Decode Secret</h5>
            <pre><code class="language-bash"># Verify both objects exist in the ivolve namespace:
#   -n ivolve : Scope query to ivolve namespace
kubectl get configmap,secret -n ivolve

# Decode the secret value from the cluster to confirm:
#   -o jsonpath='{...}' : Extracts specific field from resource JSON structure
#   base64 -d           : Decodes base64 string back to plaintext
kubectl get secret ivolve-secret -n ivolve -o jsonpath='{.data.MYSQL_ROOT_PASSWORD}' | base64 -d
# Output: ivolveroot123</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>The <code>echo -n</code> Trick:</strong> If you forget <code>-n</code> and just run <code>echo 'mypassword' | base64</code>, your terminal adds an invisible newline character (<code>\\n</code>) to the end of the password. Your app will send that extra newline when logging into MySQL and authentication will mysteriously fail!</li>
                <li><strong>Is Base64 True Encryption?</strong> No! Base64 is only encoding (obfuscation), like writing in pig latin. Anyone who can run <code>kubectl get secret</code> can decode it. In production, enable <strong>etcd encryption at rest</strong> with AWS KMS or HashiCorp Vault.</li>
            </ul>
        """
    },
    {
        "id": "lab-13",
        "number": "Lab 13",
        "title": "Persistent Storage Setup for Application Logging",
        "module": "Kubernetes",
        "icon": "💾",
        "tags": ["PersistentVolume", "PVC", "ReadWriteMany", "hostPath"],
        "summary": "Ensure application logs survive container crashes by binding a hostPath PersistentVolume with a PersistentVolumeClaim.",
        "question": [
            "Define a Persistent Volume (PV) with the following specifications:",
            "  • Name: ivolvePV",
            "  • Size: 1Gi",
            "  • Storage type: hostPath",
            "  • Path: /mnt/app-logs on the node file system",
            "  • Access mode: ReadWriteMany (to allow all replicas read/write access)",
            "  • Reclaim policy: Retain",
            "Define a Persistent Volume Claim (PVC) with name ivolvePVC that requests 1Gi storage.",
            "Ensure the PVC access mode matches the PV (ReadWriteMany).",
            "Do not use any StorageClass."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Containers are temporary (ephemeral). When a container restarts, crashes, or updates to a new version, every file written inside it is deleted.</p>
            <p>If your app writes access logs to <code>/app/logs</code>, you will lose all audit history whenever a pod restarts. Kubernetes solves this by separating storage into two roles:</p>
            <ul>
                <li><strong>PersistentVolume (PV) - The Hard Drive:</strong> A real storage volume created on the cluster. In this lab, it points to a real folder on the physical node (<code>/mnt/app-logs</code>).</li>
                <li><strong>PersistentVolumeClaim (PVC) - The Voucher / Request:</strong> The application developer does not need to know where the physical hard drive is. They just say: <em>"I need a 1 GB drive with ReadWriteMany access."</em></li>
                <li><strong>The Binding:</strong> Kubernetes automatically finds a PV that matches the PVC's request and permanently marries them together (Status: <code>Bound</code>).</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Host System</span>
                    <span class="node-title">/mnt/app-logs</span>
                    <span class="node-sub">Physical Disk Path</span>
                </div>
                <div class="flow-arrow">➔ Mapped to ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Cluster Storage</span>
                    <span class="node-title">PV: ivolve-pv</span>
                    <span class="node-sub">1Gi, ReadWriteMany</span>
                </div>
                <div class="flow-arrow">➔ Bound to ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Namespace Request</span>
                    <span class="node-title">PVC: ivolve-pvc</span>
                    <span class="node-sub">Mounts to /app/logs</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create Unified PV and PVC Manifest</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab13/pv-pvc.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab13/pv-pvc.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: PersistentVolume
metadata:
  name: ivolve-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany                    # Allows multiple pods to write logs simultaneously
  persistentVolumeReclaimPolicy: Retain # Keeps data safe if the PVC is deleted
  storageClassName: ""                 # Empty string forces static binding!
  hostPath:
    path: /mnt/app-logs
    type: DirectoryOrCreate
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ivolve-pvc
  namespace: ivolve
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: ""                 # Must match the PV's empty storageClassName
  resources:
    requests:
      storage: 1Gi</code></pre>

            <h5>2. Apply and Verify the Binding</h5>
            <pre><code class="language-bash">kubectl apply -f pv-pvc.yaml

# Check status of both objects:
kubectl get pv,pvc -n ivolve</code></pre>
            <div class="terminal-output">
NAME                         CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM
persistentvolume/ivolve-pv   1Gi        RWX            Retain           Bound    ivolve/ivolve-pvc

NAME                               STATUS   VOLUME      CAPACITY   ACCESS MODES
persistentvolumeclaim/ivolve-pvc   Bound    ivolve-pv   1Gi        RWX
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>The <code>storageClassName: ""</code> Trap:</strong> If you omit <code>storageClassName</code> on the PVC, the cluster's automatic cloud provisioner will hijack the request, create a brand-new dynamic disk, and ignore your manual <code>ivolve-pv</code>! Setting <code>storageClassName: ""</code> is the only way to tell Kubernetes: <em>"Do not use automatic provisioning; bind to my manual PV."</em></li>
            </ul>
        """
    },
    {
        "id": "lab-14",
        "number": "Lab 14",
        "title": "StatefulSet with Headless Service",
        "module": "Kubernetes",
        "icon": "🗄️",
        "tags": ["StatefulSet", "Headless Service", "MySQL 8.0", "CoreDNS"],
        "summary": "Deploy a MySQL database with a predictable network name and permanent storage using StatefulSets and a Headless Service.",
        "question": [
            "Create ivolveDB StatefulSet in ivolve ns with 1 replica running MySQL.",
            "Configure the StatefulSet pod to consume environment variables from the ConfigMap and Secret.",
            "Add node selector to ensure the pod will run on node with label 'project=ivolve'.",
            "Add a toleration to the StatefulSet with key-value 'workload=ivolveApp' and effect NoSchedule.",
            "Configure a Persistent Volume Claim (PVC) template to mount /var/lib/mysql in the pod.",
            "Write a YAML manifest for a headless service with name ivolveDBSvc targeting the MySQL StatefulSet pod.",
            "Confirm the database is operational by connecting with a MySQL client.",
            "Verify Mysql pod DNS resolution inside the cluster."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Why can't we use a normal Deployment for a database like MySQL?</p>
            <ul>
                <li><strong>Deployments are for Anonymous Workers:</strong> In a Deployment, pods get random names (like <code>app-7dfb8-xk2</code>). If a pod dies, the replacement gets a new random name. That's fine for web servers, but terrible for databases.</li>
                <li><strong>StatefulSets are for Identifiable Leaders:</strong> In a StatefulSet, pods get ordered, predictable names starting from 0: <code>ivolve-db-0</code>. If <code>ivolve-db-0</code> crashes, it is recreated with the exact same name <code>ivolve-db-0</code> and automatically re-attaches to its exact same hard drive!</li>
                <li><strong>What is a Headless Service?</strong> A normal Kubernetes service gives you one shared IP that randomly balances traffic. A <strong>Headless Service</strong> (<code>clusterIP: None</code>) tells the internal CoreDNS server: <em>"Give this specific database pod its own direct DNS name: <code>ivolve-db-0.ivolve-db-svc.ivolve.svc.cluster.local</code>."</em></li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Direct DNS</span>
                    <span class="node-title">Headless Service</span>
                    <span class="node-sub">clusterIP: None</span>
                </div>
                <div class="flow-arrow">➔ Predictable FQDN ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Pod Identity</span>
                    <span class="node-title">ivolve-db-0</span>
                    <span class="node-sub">StatefulSet (MySQL 8.0)</span>
                </div>
                <div class="flow-arrow">➔ Injects ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Config & Data</span>
                    <span class="node-title">CM + Secret + PVC</span>
                    <span class="node-sub">Mounted /var/lib/mysql</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create the Manifest</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab14/statefulset.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab14/statefulset.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: Service
metadata:
  name: ivolve-db-svc                  # The Headless Service
  namespace: ivolve
spec:
  clusterIP: None                      # clusterIP: None makes it Headless!
  selector:
    app: ivolve-db
  ports:
    - port: 3306
      name: mysql
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ivolve-db
  namespace: ivolve
spec:
  serviceName: ivolve-db-svc           # Must match the Headless Service name!
  replicas: 1
  selector:
    matchLabels:
      app: ivolve-db
  template:
    metadata:
      labels:
        app: ivolve-db
    spec:
      nodeSelector:
        project: ivolve                # Target the isolated node from Lab 10
      tolerations:
        - key: "workload"
          operator: "Equal"
          value: "ivolveApp"
          effect: "NoSchedule"
      containers:
        - name: mysql
          image: mysql:8.0
          ports:
            - containerPort: 3306
              name: mysql
          envFrom:
            - configMapRef:
                name: ivolve-cm        # Load DB_HOST and DB_USER from Lab 12
            - secretRef:
                name: ivolve-secret    # Load passwords from Lab 12
          volumeMounts:
            - name: mysql-data
              mountPath: /var/lib/mysql
  volumeClaimTemplates:
    - metadata:
        name: mysql-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi</code></pre>

            <h5>2. Apply and Wait for Ready</h5>
            <pre><code class="language-bash"># Apply StatefulSet and Headless Service manifests:
kubectl apply -f statefulset.yaml

# Wait until MySQL pod initializes storage and passes readiness probes:
#   --for=condition=Ready : Blocks execution until Pod condition equals Ready
#   --timeout=180s        : Aborts with error if pod fails to initialize within 3 minutes
kubectl wait --for=condition=Ready pod/ivolve-db-0 -n ivolve --timeout=180s</code></pre>

            <h5>3. Verify Placement and Database Operation</h5>
            <pre><code class="language-bash"># Verify the pod landed on the tainted desktop-worker:
#   -o wide : Displays node assignment (desktop-worker) and pod IP
kubectl get pods -n ivolve -o wide
# Output shows ivolve-db-0 on desktop-worker

# Run a query directly inside MySQL database container:
#   exec ivolve-db-0 : Targets pod instance
#   --               : Separates kubectl arguments from inner container command
#   -uroot -p...     : MySQL credentials
#   -e "..."         : Executes SQL query string non-interactively
kubectl exec ivolve-db-0 -n ivolve -- mysql -uroot -pivolveroot123 -e "SHOW DATABASES;"
# Lists: information_schema, ivolve, mysql, performance_schema, sys</code></pre>

            <h5>4. Verify In-Cluster Headless DNS Name</h5>
            <pre><code class="language-bash"># Connect through the full DNS domain name provided by Headless Service:
#   -h &lt;FQDN&gt; : Connects via CoreDNS hostname: &lt;pod&gt;.&lt;service&gt;.&lt;ns&gt;.svc.cluster.local
kubectl exec ivolve-db-0 -n ivolve -- \
  mysql -h ivolve-db-0.ivolve-db-svc.ivolve.svc.cluster.local -uroot -pivolveroot123 \
  -e "SELECT @@hostname;"
# Output: ivolve-db-0 (DNS resolution confirmed working!)</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Naming Matching Rule:</strong> The <code>serviceName</code> under <code>spec</code> in the StatefulSet must exactly match the <code>metadata.name</code> of your Headless Service. If you misspell it, the pod will run, but internal DNS records will never be registered!</li>
                <li><strong>Persistent Storage Safety:</strong> When you delete a StatefulSet, Kubernetes intentionally leaves the PVCs untouched. This prevents you from accidentally wiping out your company's production database with one command.</li>
            </ul>
        """
    },
    {
        "id": "lab-15",
        "number": "Lab 15",
        "title": "Node.js Application Deployment with ClusterIP service",
        "module": "Kubernetes",
        "icon": "🚀",
        "tags": ["Deployment", "Init Containers", "ClusterIP Service", "Self-Healing"],
        "summary": "Deploy two replicas of the Node.js application, use an Init Container to automatically initialize the MySQL database schema, and expose it internally with a ClusterIP service.",
        "question": [
            "Create a Deployment named ivolveApp in ivolve ns with 2 replicas.",
            "Use your custom Docker image from Docker Hub created in Lab 8.",
            "Configure the pods to consume environment variables from the existing ConfigMap and Secret.",
            "Add a node selector to schedule pods on nodes labeled project=ivolve.",
            "Add a toleration with key workload, value ivolveApp, and effect NoSchedule.",
            "Configure the pods to use the PersistentVolume created in Lab 13.",
            "Add an init container using a MySQL client image to create the ivolve database and grant the application user the necessary privileges.",
            "Pass the database connection parameters to the init container using environment variables from the ConfigMap and Secret.",
            "Create a ClusterIP Service named ivolvaAppSvc in ivolve ns to distribute traffic across the available application pods.",
            "Connect to MySQL manually to verify that the ivolve database was created and the application user has the required privileges.",
            "Check the application logs to verify that the Node.js application successfully connects to MySQL and accesses the ivolve database."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Now that our MySQL database is running from Lab 14, we are ready to deploy our Node.js web app. But there is a classic timing problem:</p>
            <ul>
                <li><strong>The Problem:</strong> When the Node.js app boots, it expects the <code>ivolve</code> database and user privileges to already exist. If MySQL isn't ready or the user isn't created, the Node app crashes instantly.</li>
                <li><strong>The Solution (Init Containers):</strong> An <strong>Init Container</strong> is a helper container that runs <em>first</em> before your main app container starts.
                    <br>&bull; The helper container connects to MySQL, runs <code>CREATE DATABASE IF NOT EXISTS ivolve;</code>, grants permissions, and then gracefully exits.
                    <br>&bull; Only after the helper container finishes with success does Kubernetes start your Node.js application!</li>
                <li><strong>ClusterIP Service:</strong> A private internal load balancer. It gives you one stable IP (e.g. <code>ivolve-app-svc:3000</code>) that automatically shares traffic equally between the two app replicas.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Step 1 (First)</span>
                    <span class="node-title">Init Container</span>
                    <span class="node-sub">Seeds MySQL Database</span>
                </div>
                <div class="flow-arrow">➔ Exits 0 ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Step 2 (Main)</span>
                    <span class="node-title">Node.js App</span>
                    <span class="node-sub">2 Replicas on Port 3000</span>
                </div>
                <div class="flow-arrow">➔ Balance ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Internal Gateway</span>
                    <span class="node-title">ClusterIP Service</span>
                    <span class="node-sub">ivolve-app-svc</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create the Deployment and Service Manifest</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab15/deployment.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab15/deployment.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: Service
metadata:
  name: ivolve-app-svc                 # ClusterIP Service for application
  namespace: ivolve
spec:
  type: ClusterIP
  selector:
    app: ivolve-app
  ports:
    - port: 3000
      targetPort: 3000
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ivolve-app
  namespace: ivolve
spec:
  replicas: 2                          # Run 2 copies for high availability
  selector:
    matchLabels:
      app: ivolve-app
  template:
    metadata:
      labels:
        app: ivolve-app
    spec:
      nodeSelector:
        project: ivolve
      tolerations:
        - key: "workload"
          operator: "Equal"
          value: "ivolveApp"
          effect: "NoSchedule"
      initContainers:                  # Runs before the app starts
        - name: init-db
          image: mysql:8.0
          envFrom:
            - configMapRef:
                name: ivolve-cm
            - secretRef:
                name: ivolve-secret
          command:
            - sh
            - -c
            - |
              mysql -h $DB_HOST -uroot -p$MYSQL_ROOT_PASSWORD <<EOF
              CREATE DATABASE IF NOT EXISTS ivolve;
              CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';
              GRANT ALL PRIVILEGES ON ivolve.* TO '$DB_USER'@'%';
              FLUSH PRIVILEGES;
              EOF
      containers:
        - name: app
          image: abdalrahmanx/ivolve-app:v1  # Image pushed in Lab 8!
          ports:
            - containerPort: 3000
          envFrom:
            - configMapRef:
                name: ivolve-cm
            - secretRef:
                name: ivolve-secret
          volumeMounts:
            - name: logs
              mountPath: /app/logs
      volumes:
        - name: logs
          persistentVolumeClaim:
            claimName: ivolve-pvc      # Logging PVC from Lab 13</code></pre>

            <h5>2. Apply and Verify Rollout</h5>
            <pre><code class="language-bash"># Apply Deployment and ClusterIP Service manifests:
kubectl apply -f deployment.yaml

# Watch deployment rollout progress until both replica pods are running:
#   rollout status : Streams rollout updates and exits 0 when replica count matches spec
kubectl rollout status deployment/ivolve-app -n ivolve</code></pre>

            <h5>3. Functional Checks</h5>
            <pre><code class="language-bash"># Check app logs to verify clean database connection:
#   -c app    : Selects the main application container (skipping init-db)
#   --tail=10 : Displays only the last 10 log lines
kubectl logs deployment/ivolve-app -n ivolve -c app --tail=10
# Shows: "Connected to MySQL and 'ivolve' DB found. Server started on http://0.0.0.0:3000"

# Test response from the internal ClusterIP service via cluster DNS:
#   exec deployment/... : Selects one running pod from deployment
#   -c app              : Specifies target container
#   wget -qO-           : -q quiet mode, -O- prints response body directly to stdout
kubectl exec deployment/ivolve-app -n ivolve -c app -- wget -qO- http://ivolve-app-svc:3000/health
# Output: iVolve web app is working! Keep calm and code on!</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>ConfigMap DNS Fix:</strong> Make sure the <code>DB_HOST</code> inside your Lab 12 ConfigMap is set to <code>ivolve-db-svc.ivolve.svc.cluster.local</code> (the headless service name from Lab 14). If it was set to something generic like <code>mysql</code>, the app will never find the database.</li>
            </ul>
        """
    },
    {
        "id": "lab-16",
        "number": "Lab 16",
        "title": "Pod Resource Management with CPU and Memory Requests and Limits",
        "module": "Kubernetes",
        "icon": "📊",
        "tags": ["Resource Limits", "QoS", "Metrics-Server", "Quota Deadlock"],
        "summary": "Set CPU and RAM requests and limits on your deployment, solve the rolling update quota deadlock, and monitor live consumption with metrics-server.",
        "question": [
            "Update the existing ivolveApp Deployment to include resource requests and limits.",
            "Resource Requests:",
            "  ✓ cpu: 1 (1 vCPU)",
            "  ✓ memory: 1Gi",
            "Resource Limits:",
            "  ✓ cpu: 2 (2 vCPUs)",
            "  ✓ memory: 2Gi",
            "Use kubectl describe pod to verify the applied resource requests and limits.",
            "Use kubectl top pod to monitor real-time resource usage (metric server must be running in the cluster)."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>How does Kubernetes keep pods from fighting over CPU and memory?</p>
            <ul>
                <li><strong>Requests (The Guaranteed Reservation):</strong> This is the <em>minimum</em> amount of CPU and RAM your pod needs to survive. The scheduler uses requests to find a node that has enough spare room.</li>
                <li><strong>Limits (The Ceiling):</strong> This is the <em>maximum</em> amount your pod is allowed to use. If your pod tries to consume more CPU than its limit, Linux throttles it. If it tries to consume more memory than its limit, Linux terminates it (OOMKilled).</li>
                <li><strong>The Rolling Update Quota Deadlock:</strong>
                    <br>&bull; In Lab 11, we set a ResourceQuota of <strong>3 pods maximum</strong>.
                    <br>&bull; Currently running: 2 app pods + 1 MySQL pod = 3 pods (100% full).
                    <br>&bull; When you update a Deployment, Kubernetes starts a <em>new surge pod</em> before killing the old one to avoid downtime.
                    <br>&bull; But the 4th pod is <strong>rejected</strong> by the quota! The deployment gets stuck in a deadlock until you increase the namespace quota headroom to 5 pods.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Quota Problem</span>
                    <span class="node-title">3/3 Pods Full</span>
                    <span class="node-sub">Surge Pod Blocked!</span>
                </div>
                <div class="flow-arrow">➔ Patch Quota ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Headroom Added</span>
                    <span class="node-title">Quota: 5 Pods</span>
                    <span class="node-sub">Rollout Completes</span>
                </div>
                <div class="flow-arrow">➔ Verify ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Live Monitoring</span>
                    <span class="node-title">kubectl top pod</span>
                    <span class="node-sub">Shows real CPU & RAM</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Add Resources to the Deployment</h5>
            <pre><code class="language-yaml"># Added inside deployment.yaml under spec.template.spec.containers[0]:
resources:
  requests:
    cpu: "1"
    memory: "1Gi"
  limits:
    cpu: "2"
    memory: "2Gi"</code></pre>

            <h5>2. Solve the Quota Deadlock</h5>
            <p>When applying the update, Kubernetes attempts to create a surge pod and fails with:</p>
            <div class="terminal-output">
FailedCreate: exceeded quota: ivolve-quota, requested: pods=1, used: pods=3, limited: pods=3
            </div>
            <p>Increase the namespace quota from 3 to 5 to allow rolling update headroom:</p>
            <pre><code class="language-bash"># Update the pod limit to 5 in resourcequota.yaml and re-apply:
# (Or run 'kubectl edit resourcequota ivolve-quota -n ivolve' and set pods: "5")
sed -i 's/pods: "3"/pods: "5"/' ../Lab11/resourcequota.yaml
kubectl apply -f ../Lab11/resourcequota.yaml

# Apply the updated deployment with resource requests and limits:
kubectl apply -f deployment.yaml
kubectl rollout status deployment/ivolve-app -n ivolve</code></pre>

            <h5>3. Install Metrics-Server</h5>
            <p>Download the official manifest, add the <code>--kubelet-insecure-tls</code> flag to container args (required for self-signed kubelet certificates), and apply:</p>
            <pre><code class="language-bash"># Download official Kubernetes SIGs metrics-server manifest:
curl -LO https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Add --kubelet-insecure-tls argument for local/kubeadm self-signed certificates:
sed -i '/--kubelet-preferred-address-types/a \\        - --kubelet-insecure-tls' components.yaml

# Deploy metrics-server:
kubectl apply -f components.yaml</code></pre>

            <h5>4. Verify Live Resource Usage</h5>
            <pre><code class="language-bash"># Verify limits configured on deployment:
#   grep -A5 Limits : Shows matching line plus 5 following lines of limits configuration
kubectl describe deployment ivolve-app -n ivolve | grep -A5 Limits

# Monitor real-time CPU and memory usage of running pods:
#   top pod : Queries metrics-server for current CPU (cores/millicores) and RAM bytes
kubectl top pod -n ivolve</code></pre>
            <div class="terminal-output">
NAME                          CPU(cores)   MEMORY(bytes)
ivolve-app-5d4c4c8d8c-mmnlm   1m           22Mi
ivolve-app-5d4c4c8d8c-ndtz4   1m           21Mi
ivolve-db-0                   8m           370Mi
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Why does the app only use 21 MiB?</strong> Notice that the app uses ~21 MiB while we requested 1 GiB. Remember: <em>requests are not what the app is currently using—they are what is reserved on the server</em> to ensure the pod never starves during peak traffic.</li>
            </ul>
        """
    },
    {
        "id": "lab-17",
        "number": "Lab 17",
        "title": "Control Pod-to-Pod Traffic via Network Policy",
        "module": "Kubernetes",
        "icon": "🔒",
        "tags": ["NetworkPolicy", "Zero-Trust", "Firewall", "Port 3306"],
        "summary": "Block unauthorized access to MySQL by creating an in-cluster firewall policy that allows traffic only from your Node.js application pods.",
        "question": [
            "Define a Network Policy with the following specifications:",
            "  • Name: ivolveNP",
            "  • Pod Selector: Targets mysql pod.",
            "  • Policy Types: Only Ingress",
            "  • Ingress Rule:",
            "      ✓ Allows traffic only from the application pods.",
            "      ✓ Restrict access to port 3306 (MySQL default port)."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>By default, Kubernetes network security is wide open: <strong>any pod in the entire cluster can connect to any other pod</strong>. If an intern or compromised app in another namespace knows MySQL's IP, they can connect directly to your database.</p>
            <p><strong>A NetworkPolicy is a firewall for Kubernetes pods:</strong></p>
            <ul>
                <li>The moment you attach a NetworkPolicy to your MySQL pod, it enters <strong>Default-Deny mode</strong>. All incoming traffic is blocked.</li>
                <li>Then you punch one single hole in the firewall: <em>"Allow traffic on port 3306, but ONLY from pods that have the label <code>app: ivolve-app</code>."</em></li>
                <li>Any other pod that tries to connect gets timed out and dropped.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-comparison">
                <div class="comparison-card">
                    <div class="comp-badge success">Authorized Pod</div>
                    <div class="comp-flow">Label: app=ivolve-app ➔ Port 3306 ➔ ALLOWED!</div>
                    <div class="comp-metric success">Connection Succeeded</div>
                    <div class="comp-note">Matches the ingress rule in ivolve-np.</div>
                </div>
                <div class="comparison-card">
                    <div class="comp-badge danger">Unauthorized Pod</div>
                    <div class="comp-flow">Different Label / Namespace ➔ Port 3306 ➔ DROPPED!</div>
                    <div class="comp-metric danger">Connection Timed Out</div>
                    <div class="comp-note">Blocked by Calico CNI firewall enforcement.</div>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create the NetworkPolicy Manifest</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab17/networkpolicy.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab17/networkpolicy.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ivolve-np
  namespace: ivolve
spec:
  podSelector:
    matchLabels:
      app: ivolve-db                   # Firewall protects the MySQL pod
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: ivolve-app          # ONLY pods with this label can enter!
      ports:
        - protocol: TCP
          port: 3306                   # Strictly MySQL port</code></pre>

            <h5>2. Apply and Verify</h5>
            <pre><code class="language-bash"># Apply NetworkPolicy firewall rules to cluster:
kubectl apply -f networkpolicy.yaml

# Verify NetworkPolicy is recognized by CNI:
kubectl get networkpolicy -n ivolve</code></pre>
            <div class="terminal-output">
NAME        POD-SELECTOR    AGE
ivolve-np   app=ivolve-db   10s
            </div>

            <h5>3. Functional Verification</h5>
            <pre><code class="language-bash"># Test 1: Connection from authorized application pod (ALLOWED):
#   -c app      : Target Node.js application container
#   nc -zvw3    : Netcat flags:
#                 -z : Zero-I/O mode (port scan without transmitting payload)
#                 -v : Verbose status output
#                 -w3: Timeout after 3 seconds if packet blocked
kubectl exec deployment/ivolve-app -n ivolve -c app -- nc -zvw3 ivolve-db-svc 3306
# Output: Connection to ivolve-db-svc 3306 port [tcp/mysql] succeeded!

# Test 2: Connection from unauthorized pod in default namespace (BLOCKED on Calico):
#   --rm -it    : Ephemeral interactive container deleted immediately upon exit
kubectl run rogue --image=busybox -n default --rm -it -- nc -zvw3 10.244.2.3 3306
# Output: Connection timed out! (Packets dropped by Calico iptables filter)</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>CNI Requirement:</strong> Remember from Lab 9: Kubernetes itself does not filter packets. An active CNI like <strong>Calico</strong> or <strong>Cilium</strong> must be installed to enforce NetworkPolicies. On default Kind/Docker-Desktop clusters without Calico, the manifest is saved, but packets aren't filtered.</li>
            </ul>
        """
    },
    {
        "id": "lab-18",
        "number": "Lab 18",
        "title": "Node-Wide Pod Management with DaemonSet & Cluster Monitoring",
        "module": "Kubernetes",
        "icon": "📈",
        "tags": ["DaemonSet", "Prometheus", "Grafana", "node-exporter", "Alertmanager"],
        "summary": "Deploy a complete monitoring system using a DaemonSet to collect machine hardware metrics across every server and graph them in Grafana.",
        "question": [
            "Create monitoring namespace.",
            "Deploy Prometheus in the monitoring namespace.",
            "Deploy Alert Manager in the monitoring namespace.",
            "Deploy Grafana in the monitoring namespace.",
            "Deploy a DaemonSet for Prometheus node-exporter in the monitoring namespace.",
            "Validate that a node-exporter pod is scheduled on each node.",
            "Confirm correct metrics exposure by accessing <node_IP>:9100/metrics.",
            "Configure Prometheus to collect data from node-exporter.",
            "Configure Grafana dashboard for Kubernetes."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>How do company monitoring teams know when a server's disk is 99% full or CPU is burning at 100%?</p>
            <ul>
                <li><strong>What is a DaemonSet?</strong> A normal Deployment runs 2 or 3 pods anywhere. A <strong>DaemonSet</strong> guarantees that <em>every single server in your cluster runs exactly one copy</em> of the monitoring pod. If you add 10 new servers tomorrow, Kubernetes automatically puts the monitoring pod on all 10 without you doing anything.</li>
                <li><strong>The 4 Pieces of the Monitoring Stack:</strong>
                    <ol>
                        <li><strong>node-exporter (The Sensor):</strong> A DaemonSet pod that reads Linux CPU, RAM, and disk metrics and exposes them at <code>:9100/metrics</code>.</li>
                        <li><strong>Prometheus (The Database & Collector):</strong> Periodically scrapes numbers from every node-exporter and saves them over time.</li>
                        <li><strong>Alertmanager (The Siren):</strong> Sends an alert (Slack, email, SMS) if a server crashes.</li>
                        <li><strong>Grafana (The Dashboard):</strong> Draws beautiful interactive graphs and charts so you can see your servers live on screen.</li>
                    </ol>
                </li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Every Node</span>
                    <span class="node-title">node-exporter</span>
                    <span class="node-sub">Port 9100 Metrics</span>
                </div>
                <div class="flow-arrow">➔ Scrapes Every 15s ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Time-Series DB</span>
                    <span class="node-title">Prometheus</span>
                    <span class="node-sub">Stores Cluster Health</span>
                </div>
                <div class="flow-arrow">➔ Feeds ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Visualization</span>
                    <span class="node-title">Grafana</span>
                    <span class="node-sub">Dashboard #1860</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Deploy Monitoring Namespace and node-exporter DaemonSet</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab18/01-node-exporter.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab18/01-node-exporter.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      hostNetwork: true                # Reads real host networking
      hostPID: true
      tolerations:
        - operator: "Exists"          # Ensures it lands on master/control-plane nodes too
      containers:
        - name: node-exporter
          image: prom/node-exporter:v1.8.1
          ports:
            - containerPort: 9100
              hostPort: 9100
          volumeMounts:
            - name: proc
              mountPath: /host/proc
              readOnly: true
            - name: sys
              mountPath: /host/sys
              readOnly: true
      volumes:
        - name: proc
          hostPath: { path: /proc }
        - name: sys
          hostPath: { path: /sys }</code></pre>

            <h5>2. Apply the Complete Observability Stack</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab18/02-prometheus.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>02-prometheus.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
                <a href="Kubernetes/Lab18/03-alertmanager.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>03-alertmanager.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
                <a href="Kubernetes/Lab18/04-grafana.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>04-grafana.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-bash"># Apply complete monitoring stack manifests:
kubectl apply -f 00-namespace-rbac.yaml -f 01-node-exporter.yaml -f 02-prometheus.yaml -f 03-alertmanager.yaml -f 04-grafana.yaml

# Import the popular Node Exporter Full Dashboard (ID 1860) JSON into Grafana:
#   --from-file : Loads entire JSON dashboard file into a ConfigMap key
kubectl create configmap grafana-dashboard-k8s -n monitoring --from-file=node-exporter-full.json

# Trigger rolling restart to mount the new dashboard ConfigMap into Grafana pod:
#   rollout restart : Gracefully terminates existing pods and launches replacements with new volume mounts
kubectl rollout restart deployment/grafana -n monitoring</code></pre>

            <h5>3. Access Grafana Live Dashboard</h5>
            <pre><code class="language-bash"># Forward local workstation port to Grafana service inside cluster:
#   -n monitoring     : Target monitoring namespace
#   svc/grafana       : Kubernetes Service object
#   3000:3000         : Maps local port 3000 to remote Service port 3000
kubectl port-forward -n monitoring svc/grafana 3000:3000</code></pre>
            <p>Open <code>http://localhost:3000</code> in your browser (Username: <code>admin</code>, Password: <code>admin</code>). Click on Dashboards &rarr; "Node Exporter Full" to view live graphs of all nodes!</p>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Image Name Mistake:</strong> Be careful with Docker image names: the official image is <code>prom/node-exporter</code>. If you accidentally write <code>prometheus/node-exporter</code>, that repo doesn't exist and your pods will get stuck in <code>ImagePullBackOff</code>!</li>
                <li><strong>Control Plane Toleration:</strong> If your master node has the <code>control-plane:NoSchedule</code> taint, normal pods won't land on it. Adding <code>tolerations: [{operator: Exists}]</code> ensures you monitor your master node hardware too.</li>
            </ul>
        """
    },
    {
        "id": "lab-19",
        "number": "Lab 19",
        "title": "Securing Kubernetes with RBAC and Service Accounts",
        "module": "Kubernetes",
        "icon": "🛡️",
        "tags": ["RBAC", "ServiceAccount", "Least Privilege", "RoleBinding"],
        "summary": "Create a strictly limited service account token for automated CI systems (like Jenkins) that can only touch Deployments in the ivolve namespace.",
        "question": [
            "Create jenkinsSA Service Account in the ivolve namespace.",
            "Create a token for the service account.",
            "Define a Role named ivolveDeployRole that grants create/update permissions on deployment in the ivolve namespace.",
            "Create a Role Binding with name ivolveDeployRoleBinding to bind the ivolveDeployRole role to the jenkinsSA service account.",
            "Validate the role can only create/update deployment in ivolve namespace."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>When you automate deployments using Jenkins or GitHub Actions, your CI server needs to communicate with Kubernetes to deploy new versions. But you should <strong>never give Jenkins cluster administrator credentials</strong>.</p>
            <p>If a hacker breaches your Jenkins server and Jenkins has admin keys, the hacker owns your whole company cluster! We apply the <strong>Principle of Least Privilege</strong>:</p>
            <ul>
                <li><strong>ServiceAccount:</strong> A user account meant for computer software (not humans). We name it <code>jenkins-sa</code>.</li>
                <li><strong>Role:</strong> A list of exact allowed actions. We say: <em>"You may ONLY create, update, get, and patch Deployments inside the ivolve namespace. You cannot delete pods, you cannot view secrets, and you cannot touch any other namespace."</em></li>
                <li><strong>RoleBinding:</strong> The chain that ties the Role to the ServiceAccount.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Identity</span>
                    <span class="node-title">jenkins-sa</span>
                    <span class="node-sub">ServiceAccount</span>
                </div>
                <div class="flow-arrow">➔ Bound via ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">RoleBinding</span>
                    <span class="node-title">ivolveDeployRole</span>
                    <span class="node-sub">Namespace: ivolve</span>
                </div>
                <div class="flow-arrow">➔ Scope Test ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Security Result</span>
                    <span class="node-title">Deployments: YES</span>
                    <span class="node-sub">Pods / Other NS: DENIED</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create the RBAC Manifest</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab19/rbac.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab19/rbac.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins-sa                     # Lowercase RFC 1123 name
  namespace: ivolve
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ivolve-deploy-role
  namespace: ivolve
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["create", "update", "get", "patch"] # get/patch are required for kubectl apply!
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ivolve-deploy-role-binding
  namespace: ivolve
subjects:
  - kind: ServiceAccount
    name: jenkins-sa
    namespace: ivolve
roleRef:
  kind: Role
  name: ivolve-deploy-role
  apiGroup: rbac.authorization.k8s.io</code></pre>
            <pre><code class="language-bash">kubectl apply -f rbac.yaml</code></pre>

            <h5>2. Create Permanent Token for Jenkins</h5>
            <div class="file-links-bar">
                <a href="Kubernetes/Lab19/jenkins-sa-token.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Kubernetes/Lab19/jenkins-sa-token.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">apiVersion: v1
kind: Secret
metadata:
  name: jenkins-sa-token
  namespace: ivolve
  annotations:
    kubernetes.io/service-account.name: jenkins-sa
type: kubernetes.io/service-account-token</code></pre>
            <pre><code class="language-bash">kubectl apply -f jenkins-sa-token.yaml</code></pre>

            <h5>3. Validate Scoped Permissions</h5>
            <pre><code class="language-bash"># Extract bearer token from Secret data:
#   -o jsonpath='{.data.token}' : Selects token field
#   base64 -d                   : Decodes Base64 to plaintext JWT token
TOKEN=$(kubectl get secret jenkins-sa-token -n ivolve -o jsonpath='{.data.token}' | base64 -d)

# Test 1: Allowed - Create a deployment in ivolve namespace:
#   --token                       : Authenticates using the extracted ServiceAccount bearer token
#   --server                      : Address of Kubernetes API server
#   --insecure-skip-tls-verify    : Bypasses self-signed cluster CA check for testing
#   -n ivolve                     : In-scope namespace
kubectl --token=$TOKEN --server=&lt;K8S_URL&gt; --insecure-skip-tls-verify \
  create deployment test-deploy --image=busybox -n ivolve
# Output: deployment.apps/test-deploy created (ALLOWED)

# Test 2: Forbidden - Attempt to create a pod directly:
kubectl --token=$TOKEN --server=&lt;K8S_URL&gt; --insecure-skip-tls-verify \
  run test-pod --image=busybox -n ivolve
# Output: Error from server (Forbidden): User cannot create resource "pods"!

# Test 3: Forbidden - Attempt to touch default namespace:
kubectl --token=$TOKEN --server=&lt;K8S_URL&gt; --insecure-skip-tls-verify \
  create deployment test-deploy --image=busybox -n default
# Output: Error from server (Forbidden): cannot create in namespace "default"!</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Why <code>get</code> and <code>patch</code> are Required:</strong> The slide says "grant create/update". But when Jenkins runs <code>kubectl apply</code>, kubectl must first <code>get</code> the current deployment from the cluster and <code>patch</code> the differences. If you forget <code>get</code> and <code>patch</code>, your pipeline will fail with a forbidden error!</li>
            </ul>
        """
    }
]
