# NTI & iVolve Cloud DevOps Accelerator — Hands-On Labs

Complete hands-on lab solutions, code, YAML manifests, and architecture walkthroughs from the **NTI & iVolve Cloud DevOps Accelerator Program**. Covers 28 practical labs across Linux build tools, containerization, orchestration, continuous delivery, GitOps, and infrastructure automation.

> 🌐 **Live Interactive Guide:** **[https://abdalrahmanx9.github.io/Ivolve-labs/](https://abdalrahmanx9.github.io/Ivolve-labs/)**
> 
> *A self-contained web dashboard detailing all 28 labs with architecture diagrams, step-by-step commands, flag explanations, and gotchas.*

---

## Curriculum & Modules

- **Build Tools (Labs 1–2):** Java application compilation, unit testing, and packaging using Apache Maven and Gradle.
- **Docker Containerization (Labs 3–8):** Writing Dockerfiles, multi-stage build optimization, Trivy vulnerability scanning & remediation, environment variables, multi-network microservices, persistent volumes, and multi-container stacks with Docker Compose.
- **Kubernetes Orchestration (Labs 9–19):** Production Kubeadm cluster setup with containerd and Calico CNI (following official `kubernetes.io` and `docs.tigera.io` docs), node isolation (taints, tolerations, nodeSelector), Namespaces, ResourceQuotas, ConfigMaps, Secrets, PersistentVolumes, MySQL StatefulSet with Headless Service, Node.js Deployments with init containers, CPU/memory limits, NetworkPolicies, observability stack (Prometheus, Alertmanager, Grafana, node-exporter DaemonSet), and RBAC ServiceAccounts.
- **Jenkins CI/CD (Labs 20–22):** Groovy Configuration-as-Code, Role-Based Matrix Authorization, 7-stage automated pipelines (Maven, Docker, Trivy, Docker Hub, Kubernetes deployment), and reusable Jenkins Shared Libraries with ephemeral Docker agents.
- **GitOps (Lab 23):** Declarative Continuous Delivery using Argo CD and Jenkins GitOps pipeline with automated self-healing, sync policies, and out-of-band drift reconciliation.
- **Ansible Automation (Labs 24–28):** Agentless infrastructure automation: SSH key pair authentication & ad-hoc modules, full stack orchestration playbooks (Docker, Kubectl, Jenkins), reusable modular roles (`ansible-galaxy`), AES-256 encrypted Ansible Vault secrets for production MySQL configuration, and AWS EC2 dynamic inventory plugin (`amazon.aws.aws_ec2`).

---

## Lab Index

| # | Topic | Lab Title | Solution |
|---|-------|-----------|----------|
| 01 | Maven | Building and Packaging Java Application with Maven | [Build Tools/Lab1](Build%20Tools/Lab1/README.md) |
| 02 | Gradle | Building and Packaging Application with Gradle | [Build Tools/Lab2](Build%20Tools/Lab2/README.md) |
| 03 | Docker | Creating a Docker Image for a Java Application | [Docker/Lab3](Docker/Lab3/README.md) |
| 04 | Docker | Docker Image Optimization and Export/Load | [Docker/Lab4](Docker/Lab4/README.md) |
| 05 | Docker | Docker Image Vulnerability Scanning with Trivy | [Docker/Lab5](Docker/Lab5/README.md) |
| 06 | Docker | Docker Environment Variables and Resource Management | [Docker/Lab6](Docker/Lab6/README.md) |
| 07 | Docker | Multi-Network Microservices, Volumes, and Bind Mounts | [Docker/Lab7](Docker/Lab7/README.md) |
| 08 | Docker Compose | Containerized Node.js and MySQL Stack | [Docker/Lab8](Docker/Lab8/README.md) |
| 09 | Kubernetes | Deploy Kubernetes Cluster using Kubeadm & Calico CNI | [Kubernetes/Lab9](Kubernetes/Lab9/README.md) |
| 10 | Kubernetes | Node Isolation Using Taints and Labels | [Kubernetes/Lab10](Kubernetes/Lab10/README.md) |
| 11 | Kubernetes | Namespace Management and Resource Quota Enforcement | [Kubernetes/Lab11](Kubernetes/Lab11/README.md) |
| 12 | Kubernetes | Managing Configuration and Secrets (ConfigMaps & Secrets) | [Kubernetes/Lab12](Kubernetes/Lab12/README.md) |
| 13 | Kubernetes | Persistent Storage Setup for Application Logging (PV & PVC) | [Kubernetes/Lab13](Kubernetes/Lab13/README.md) |
| 14 | Kubernetes | StatefulSet with Headless Service (MySQL 8.0) | [Kubernetes/Lab14](Kubernetes/Lab14/README.md) |
| 15 | Kubernetes | Node.js Application Deployment with ClusterIP Service | [Kubernetes/Lab15](Kubernetes/Lab15/README.md) |
| 16 | Kubernetes | Pod Resource Management (CPU & Memory Requests/Limits) | [Kubernetes/Lab16](Kubernetes/Lab16/README.md) |
| 17 | Kubernetes | Control Pod-to-Pod Traffic via Network Policy | [Kubernetes/Lab17](Kubernetes/Lab17/README.md) |
| 18 | Kubernetes | Node-Wide Management with DaemonSet & Prometheus/Grafana | [Kubernetes/Lab18](Kubernetes/Lab18/README.md) |
| 19 | Kubernetes | Securing Kubernetes with RBAC and Service Accounts | [Kubernetes/Lab19](Kubernetes/Lab19/README.md) |
| 20 | Jenkins | Role-Based Authorization in Jenkins | [Jenkins/Lab20](Jenkins/Lab20/README.md) |
| 21 | Jenkins | Jenkins Pipeline for Application Deployment | [Jenkins/Lab21](Jenkins/Lab21/README.md) |
| 22 | Jenkins | CI/CD Implementation with Agents and Shared Libraries | [Jenkins/Lab22](Jenkins/Lab22/README.md) |
| 23 | GitOps | GitOps Continuous Delivery with Argo CD & Jenkins | [ArgoCD/Lab23](ArgoCD/Lab23/README.md) |
| 24 | Ansible | Controller Setup, SSH Authentication & Ad-Hoc Management | [Ansible/Lab24](Ansible/Lab24/README.md) |
| 25 | Ansible | Infrastructure Automation Playbook (Docker, Kubectl & Jenkins) | [Ansible/Lab25](Ansible/Lab25/README.md) |
| 26 | Ansible | Modular Ansible Roles Architecture | [Ansible/Lab26](Ansible/Lab26/README.md) |
| 27 | Ansible | Sensitive Data Security with Ansible Vault (MySQL Role) | [Ansible/Lab27](Ansible/Lab27/README.md) |
| 28 | Ansible | AWS EC2 Dynamic Inventory & Infrastructure Orchestration | [Ansible/Lab28](Ansible/Lab28/README.md) |

---

## Directory Structure

```text
├── Build Tools/
│   ├── Lab1/                  # Maven Java calculator app
│   └── Lab2/                  # Gradle build setup
├── Docker/
│   ├── Lab3/ - Lab8/          # Dockerfiles, compose files, multi-stage configs
├── Kubernetes/
│   ├── Lab9/ - Lab19/         # Kubeadm scripts, manifests (PV/PVC, StatefulSet, RBAC, etc.)
├── Jenkins/
│   ├── Lab20/ - Lab22/        # Jenkins Configuration-as-Code, Jenkinsfiles, Shared Libs
├── ArgoCD/
│   └── Lab23/                 # Argo CD Application manifest & GitOps workflow
├── Ansible/
│   ├── Lab24/                 # Ad-hoc setup, inventory, bootstrap scripts
│   ├── Lab25/                 # Multi-tool installation playbook
│   ├── Lab26/                 # Modular roles (docker, kubectl, jenkins)
│   ├── Lab27/                 # Ansible Vault encrypted MySQL role
│   └── Lab28/                 # AWS EC2 dynamic inventory & provisioning playbook
├── index.html                 # Complete interactive single-page guide
├── robots.txt                 # Search engine crawler permissions
└── sitemap.xml                # Sitemap for search engine indexing
```

## Running the Guide Locally

You can open `index.html` directly in any web browser without needing a local web server, or view it online at [https://abdalrahmanx9.github.io/Ivolve-labs/](https://abdalrahmanx9.github.io/Ivolve-labs/).
