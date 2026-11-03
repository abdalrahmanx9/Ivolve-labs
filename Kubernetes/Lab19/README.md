# Lab 19 — RBAC with a Service Account

The idea: a Jenkins service account that can only create and update deployments in the `ivolve` namespace, nothing else. `rbac.yaml` has all three objects:

- ServiceAccount `jenkins-sa` (sheet calls it jenkinsSA, but resource names must be lowercase)
- Role `ivolve-deploy-role`: verbs create/update/get/patch on `apps/deployments`, namespace ivolve — strictly create+update per the sheet, but `kubectl apply` reads the object before writing, so get and patch are needed for a real deploy pipeline (Lab 21 hit exactly this)
- RoleBinding `ivolve-deploy-role-binding` connecting the two

Token — the modern way is a TokenRequest (`kubectl create token jenkins-sa -n ivolve`), but those expire in an hour. For a Jenkins that pushes whenever a build runs I made a long-lived token secret (`jenkins-sa-token.yaml`), which the cluster fills in automatically.

## Validating

Three tests with a kubeconfig that contains only that token.

Allowed — deployment in ivolve:

```
$ kubectl --kubeconfig jenkins-sa.kubeconfig create deployment rbac-test --image=busybox -n ivolve
deployment.apps/rbac-test created
```

Not allowed — pods:

```
Error from server (Forbidden): pods is forbidden: User "system:serviceaccount:ivolve:jenkins-sa"
cannot create resource "pods" in API group "" in the namespace "ivolve"
```

Not allowed — other namespaces:

```
Error from server (Forbidden): deployments.apps is forbidden: User "system:serviceaccount:ivolve:jenkins-sa"
cannot create resource "deployments" in API group "apps" in the namespace "default"
```

Exactly the scope the role describes.

One gotcha worth remembering: my first attempt passed the token with `kubectl --token=...` while the default kubeconfig was active, and the requests went through as kubernetes-admin anyway — the client certificate in the kubeconfig silently won over the token flag. `auth whoami` caught it. With a standalone kubeconfig file (only the token in it) the tests behave as expected.
