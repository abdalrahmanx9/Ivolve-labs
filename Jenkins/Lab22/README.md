# Lab 22 — Shared Libraries and a Jenkins Agent

Same pipeline as Lab 21, but the logic moved into a shared library and the build stage runs on an agent instead of the controller.

## The library

Three steps in `lib/vars/` — `buildApp.groovy` (mvn test + package), `buildImage.groovy` (docker build, trivy scan, login+push, rmi), `deployOnK8s.groovy` (sed the image tag into k8s.yaml, kubectl apply with the kubeconfig credential). The library lives in its own repo so Jenkins can fetch it: https://github.com/abdalrahmanx9/ivolve-jenkins-lib (pushed from the copy in this folder).

Jenkins picks it up as a global pipeline library — configured by `init.groovy.d/library.groovy` at boot:

```groovy
def source = new jenkins.plugins.git.GitSCMSource('https://github.com/abdalrahmanx9/ivolve-jenkins-lib.git')
def lib = new LibraryConfiguration('ivolve-lib', new SCMSourceRetriever(source))
lib.setDefaultVersion('main')
```

(Finding that class name took three tries — it's `jenkins.plugins.git.GitSCMSource`, with no prefix. The jars inside the git plugin were the honest source of truth.)

## The pipeline

`Jenkinsfile` shrinks to:

```groovy
@Library('ivolve-lib') _

stage('Build app') {
    agent {
        docker {
            image 'maven:3.9-eclipse-temurin-17'
            args '-v ivolve-maven-repo:/root/.m2'
            reuseNode true
        }
    }
    steps { dir('Jenkins/Lab21/DemoApp') { buildApp() } }
}
stage('Build and push image') { steps { script { buildImage("...:${BUILD_NUMBER}") } } }
stage('Deploy to Kubernetes')  { steps { script { deployOnK8s("...:${BUILD_NUMBER}") } } }
```

The maven agent is the "slave" — a container Jenkins spins up just for that stage, with a named volume caching `/root/.m2` so dependencies download once. `reuseNode true` matters: without it the agent checks the repo out into a second workspace (`demoapp@2`), builds the jar there, and the docker stage back on the controller can't find it. Two other things that bit: the agent doesn't pull its image automatically (pulled `maven:3.9-eclipse-temurin-17` once on the host), and the first boot without the volume... just worked, credit where due.

## Result

Build #3 (first with the library + agent): all stages green, `docker push abdalrahmanx/ivolve-demoapp:3` with digest, `deployment.apps/demoapp` applied, pod serving. The console output is noticeably shorter too — each stage is one library call now.
