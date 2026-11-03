# Lab 21 — Pipeline: Build to Deploy

The `demoapp` job (created by the Lab 20 seed script) pulls `Jenkinsfile` from this repo and runs the whole path from source to a running pod in the kind cluster. The app is the Spring Boot demo (vendored in `DemoApp/`).

Stages, in order:

1. **Build app** — `mvn -B package` in DemoApp, produces target/demo-0.0.1-SNAPSHOT.jar
2. **Build Docker image** — `docker build` using the repo's Dockerfile (base maven:sapmachine), tagged `abdalrahmanx/ivolve-demoapp:$BUILD_NUMBER`
3. **Scan** — trivy, HIGH/CRITICAL, report-only (`--exit-code 0`). A JDK base image always has findings; failing the build here would mean never deploying anything. In a real pipeline you'd pin a patched base or set a CVE budget.
4. **Push to DockerHub** — `docker login` with the `dockerhub` Jenkins credential, push
5. **Delete image locally** — `docker rmi`, keeps the Jenkins host clean
6. **Update deployment file** — sed replaces the image tag in `k8s.yaml` with the build number
7. **Deploy** — `kubectl apply` using the `kubeconfig` credential (the Lab 19 service account, which can create/update deployments in `ivolve` and nothing else — the RBAC lab actually gating the pipeline)

And a `post` section with `always` / `success` / `failure` messages.

## Deploy target

`k8s.yaml` — deployment + ClusterIP service in `ivolve`, image tag overwritten each build.

## Result

Build #1 through all seven stages:

```
docker push abdalrahmanx/ivolve-demoapp:1
kubectl apply -f Jenkins/Lab21/k8s.yaml
deployment.apps/demoapp configured
```

Verify on the cluster:

```
$ kubectl get pods -n ivolve -l app=demoapp
demoapp-...  1/1  Running

$ kubectl exec ... -- wget -qO- http://demoapp-svc:8080/
Hello from Dockerized Spring Boot!
```

Each new build pushes tag 2, 3, ... and updates the deployment — a rolling update each time.
