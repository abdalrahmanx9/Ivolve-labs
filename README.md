# DevOps Labs

Labs from the Ivolve DevOps training. Each lab folder holds the actual working files plus a README documenting what I did

## Labs

| # | Tool | Lab |
|---|------|-----|
| 1 | Maven | [Java app: test, package, run](Build%20Tools/Lab1/README.md) |
| 2 | Gradle | [Same app rebuilt with Gradle](Build%20Tools/Lab2/README.md) |
| 3 | Docker | [Image for the Java app, two ways](Docker/Lab3/README.md) |
| 4 | Docker | [Multi-stage optimization, save/load](Docker/Lab4/README.md) |
| 5 | Docker | [Trivy vulnerability scanning + remediation](Docker/Lab5/README.md) |
| 6 | Docker | [Env vars and resource limits](Docker/Lab6/README.md) |
| 7 | Docker | [Multi-network microservices + volumes](Docker/Lab7/README.md) |
| 8 | Docker Compose | [Node.js + MySQL stack, pushed to Docker Hub](Docker/Lab8/README.md) |

More as the course goes: Docker, Kubernetes, Jenkins, ArgoCD, Ansible.

## Layout

```
Build Tools/    Lab1 (Maven), Lab2 (Gradle), ...
Docker/         Lab3, ...
Kubernetes/     Lab5, ...
Jenkins/        Lab7, ...
ArgoCD/         Lab9, ...
Ansible/        Lab11, ...
```

Build outputs (`target/`, `build/`, `.gradle/`) are gitignored — rebuild from source with the commands in each README.
