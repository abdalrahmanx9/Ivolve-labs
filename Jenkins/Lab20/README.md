# Lab 20 — Jenkins Users and Role-Based Authorization

Jenkins runs as a Docker container on the host, built from `jenkins/Dockerfile` in this folder. On top of `jenkins/jenkins:lts-jdk17` it adds the tools the pipelines need (docker CLI, maven, kubectl, trivy) and three init scripts in `init.groovy.d/` that configure everything at first boot — no clicking through the UI:

- `security.groovy` — users + authorization
- `credentials.groovy` — dockerhub + kubeconfig credentials (from runtime env, never baked into the image)
- `seed.groovy` — creates the `demoapp` pipeline job (Lab 21)

## user1 = admin, user2 = read-only

```groovy
def realm = new HudsonPrivateSecurityRealm(false)
realm.createAccount('user1', 'admin123')
realm.createAccount('user2', 'read123')

def strategy = new GlobalMatrixAuthorizationStrategy()
strategy.add(Jenkins.ADMINISTER, 'user1')
strategy.add(Jenkins.READ, 'user2')
strategy.add(hudson.model.Item.READ, 'user2')
strategy.add(hudson.model.Item.DISCOVER, 'user2')
strategy.add(hudson.model.View.READ, 'user2')
```

user1 gets ADMINISTER (full admin). user2 gets read-only: can log in, see jobs and views, but can't build, configure, or change anything.

## Run it

```bash
docker build -t jenkins-ivolve jenkins
docker run -d --name jenkins -p 8888:8080 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$env:TEMP\opencode\jenkins.kubeconfig:/var/jenkins_extra/kubeconfig:ro" \
  -e DOCKERHUB_USER=abdalrahmanx -e DOCKERHUB_TOKEN=<token> \
  jenkins-ivolve
```

(The docker socket mount is what lets pipelines run docker; the kubeconfig mount + env is what `credentials.groovy` turns into Jenkins credentials.)

## Verify

UI at http://localhost:8888 — log in as user1 and everything is configurable; log in as user2 and the "Build Now" and configuration screens are gone, only job status and console output are visible. Through the API the same thing:

```
$ curl -u user1:admin123 .../job/demoapp/build -X POST   -> 201, build starts
$ curl -u user2:read123  .../job/demoapp/build -X POST   -> 403
```
