# .tools/generator/module5_gitops.py

LABS_MODULE_5 = [
    {
        "id": "lab-23",
        "number": "Lab 23",
        "title": "Implementing a GitOps Workflow with Jenkins and Argo CD",
        "module": "GitOps",
        "icon": "🐙",
        "tags": ["Argo CD", "GitOps", "Declarative CD", "Self-Healing"],
        "summary": "Upgrade deployment architecture to pull-based GitOps: Jenkins builds images and commits YAML updates to GitHub, while Argo CD continuously reconciles live cluster state with Git.",
        "files": [
            ("ArgoCD/Lab23/application.yaml", "Argo CD Application definition (automated sync & self-heal)"),
            ("ArgoCD/Lab23/README.md", "Lab documentation and live loop verification"),
            ("Jenkins/Lab22/shared-library/vars/deployOnK8s.groovy", "Git push deploy step in Jenkins Shared Library"),
            ("Jenkins/Lab20/jenkins/init.groovy.d/credentials.groovy", "GitHub push token credential configuration")
        ],
        "question": [
            "Install Argo CD in your Kubernetes cluster.",
            "Access the Argo CD UI and log in successfully.",
            "Connect Argo CD to your GitHub repository.",
            "Create an Argo CD Application named ivolve.",
            "Configure the application to monitor the appropriate GitHub repository and manifest directory.",
            "Configure automatic synchronization so that Argo CD automatically applies changes detected in Git.",
            "Modify the DeployOnK8s Jenkins role to Push new update files into Github repo after edit the deployment file.",
            "Trigger the Jenkins pipeline to build and publish a new application image.",
            "Confirm that Argo CD detects the changes and synchronizes the application."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>In Lab 21, Jenkins connected to Kubernetes and executed <code>kubectl apply</code> directly. That is the traditional <strong>Push Model</strong>. While functional, modern cloud-native architectures transition to GitOps for two key reasons:</p>
            <ul>
                <li><strong>Credential Decoupling:</strong> The CI runner does not hold cluster admin credentials. If CI is compromised, cluster access remains protected.</li>
                <li><strong>Drift Prevention:</strong> If someone manually modifies or deletes a workload in the cluster, push-based CI never notices. GitOps continuously reconciles cluster state against Git.</li>
            </ul>
            <p><strong>The GitOps Pull Loop:</strong></p>
            <ul>
                <li><strong>Git is the Single Source of Truth:</strong> Workload manifests in Git define exactly what should run in production.</li>
                <li><strong>In-Cluster Controller:</strong> Argo CD runs inside Kubernetes, polls Git, and applies diffs automatically.</li>
                <li><strong>Clean Hand-Off:</strong> Jenkins builds and publishes the container image, updates the image tag in <code>Jenkins/Lab21/k8s.yaml</code>, and executes <code>git push</code>. Argo CD detects the commit and rolls out the change.</li>
                <li><strong>Self-Healing:</strong> If an engineer manually alters a pod or deployment via <code>kubectl</code>, Argo CD detects the drift and immediately restores the manifest from Git.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">1. CI Pipeline</span>
                    <span class="node-title">Jenkins</span>
                    <span class="node-sub">Builds image & commits YAML</span>
                </div>
                <div class="flow-arrow">➔ git push ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">2. Single Source</span>
                    <span class="node-title">GitHub Repo</span>
                    <span class="node-sub">k8s.yaml updated</span>
                </div>
                <div class="flow-arrow">➔ Polls & Syncs ➔</div>
                <div class="flow-node success">
                    <span class="node-step">3. In-Cluster CD</span>
                    <span class="node-title">Argo CD</span>
                    <span class="node-sub">Automated & Self-Healing</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Install Argo CD into the Cluster</h5>
            <pre><code class="language-bash"># Create dedicated namespace for Argo CD components:
kubectl create namespace argocd

# Apply official Argo CD manifests:
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait until all Argo CD control plane pods are running:
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s</code></pre>

            <h5>2. Access UI and Retrieve Initial Admin Password</h5>
            <pre><code class="language-bash"># Forward Argo CD API server to local port 8081:
#   8081:443 : Maps local port 8081 to container HTTPS port 443
kubectl port-forward svc/argocd-server -n argocd 8081:443 &

# Extract and decode initial admin password:
#   -o jsonpath : Retrieves password field from Secret
#   base64 -d   : Decodes base64 payload to plaintext
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo ""</code></pre>
            <p>Log in at <code>https://localhost:8081</code> using username <code>admin</code> and the decoded password.</p>

            <h5>3. Connect GitHub Repository</h5>
            <pre><code class="language-bash"># Register repository with Argo CD CLI (public repo requires no auth):
#   repo add : Registers source repository URL
argocd repo add https://github.com/abdalrahmanx9/Ivolve-labs.git</code></pre>

            <h5>4. Deploy the Argo CD Application Manifest</h5>
            <p>Define the declarative application targeting the manifests in <code>Jenkins/Lab21</code>:</p>
            <pre><code class="language-yaml">apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ivolve
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/abdalrahmanx9/Ivolve-labs.git
    targetRevision: main
    path: Jenkins/Lab21
  destination:
    server: https://kubernetes.default.svc
    namespace: ivolve
  syncPolicy:
    automated:
      selfHeal: true</code></pre>
            <pre><code class="language-bash"># Apply application definition:
kubectl apply -f ArgoCD/Lab23/application.yaml</code></pre>

            <h5>5. Update Jenkins Deploy Step to Push to Git</h5>
            <p>Update <code>Jenkins/Lab22/shared-library/vars/deployOnK8s.groovy</code> to edit the manifest and commit back to GitHub:</p>
            <pre><code class="language-groovy">def call(String image) {
    sh "sed -i 's|image: abdalrahmanx/ivolve-demoapp:.*|image: ${image}|' Jenkins/Lab21/k8s.yaml"
    sh "grep image: Jenkins/Lab21/k8s.yaml"
    withCredentials([usernamePassword(credentialsId: 'github-push',
            usernameVariable: 'USR', passwordVariable: 'PSW')]) {
        sh 'git config user.email "jenkins@ivolve.local"'
        sh 'git config user.name "jenkins"'
        sh "git add Jenkins/Lab21/k8s.yaml"
        sh "git commit -m 'ci: deploy demoapp ${image}' || echo 'nothing to commit'"
        sh 'git push https://$USR:$PSW@github.com/abdalrahmanx9/Ivolve-labs.git HEAD:main'
    }
}</code></pre>

            <h5>6. Verify Synchronization and Self-Healing</h5>
            <pre><code class="language-bash"># Check Argo CD sync status:
argocd app get ivolve

# Verify live deployment reflects the committed image:
kubectl get deployment demoapp -n ivolve -o jsonpath='{.spec.template.spec.containers[0].image}'</code></pre>
            <div class="terminal-output">
Sync Status:   Synced to (42305ff)
Health Status: Healthy
abdalrahmanx/ivolve-demoapp:1
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>No Cluster Credentials in CI:</strong> The <code>kubectl apply</code> step is removed from Jenkins entirely. Jenkins only needs Git write permissions, isolating cluster control plane credentials from the CI runner.</li>
                <li><strong>Stale Committed Tags:</strong> Ensure the initial committed manifest in Git references a valid, pushable image tag before activating automated sync, preventing ImagePullBackOff loops.</li>
            </ul>
        """
    }
]

