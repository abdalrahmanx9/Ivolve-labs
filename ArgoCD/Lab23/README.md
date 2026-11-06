# Lab 23 — GitOps with Jenkins and Argo CD

Argo CD installed from the official manifest (v3.6.1) into an `argocd` namespace. UI on https://localhost:8081 via `kubectl port-forward`, admin password from `argocd-initial-admin-secret`. Repo connected with `argocd repo add` (public repo, no credentials needed).

## The Application

```
argocd app create ivolve \
  --repo https://github.com/abdalrahmanx9/Ivolve-labs.git \
  --path Jenkins/Lab21 \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace ivolve \
  --sync-policy automated --self-heal
```

It watches `Jenkins/Lab21/` in the labs repo — where the demoapp deployment manifest lives — with automatic synchronization.

## The changed deploy step

The Lab 22 `deployOnK8s` role used to run `kubectl apply` from Jenkins. That's not GitOps — the manifest in Git went stale the moment the pipeline deployed. So the shared library step now does a `git push` instead:

```groovy
git add Jenkins/Lab21/k8s.yaml
git commit -m "ci: deploy demoapp ${image}"
git push https://$USR:$PSW@github.com/abdalrahmanx9/Ivolve-labs.git HEAD:main
```

with a `github-push` Jenkins credential (created at boot from the container's `GITHUB_TOKEN` env — `credentials.groovy`).

## The loop, observed live

1. Triggered the pipeline: builds image `:1`, pushes to Docker Hub, seds `k8s.yaml`, commits `ci: deploy demoapp ...:1` and pushes to GitHub
2. Argo CD notices the new commit within seconds and syncs on its own
3. Cluster state follows Git:

```
$ argocd app get ivolve
Sync Status:   Synced to (42305ff)
Health Status: Healthy

$ kubectl get deployment demoapp -n ivolve -o jsonpath='{.spec.template.spec.containers[0].image}'
abdalrahmanx/ivolve-demoapp:1
```

Same `kubectl apply` call is gone from the pipeline entirely — deployment now happens because Git changed. Arguably the cleanest lab in the set.

(One bump: the Application initially pulled the repo's committed image tag, which was stale and unpullable — updated the committed `k8s.yaml` to the last pushed tag first, then re-enabled the loop. Argo CD synced my fix automatically too.)
