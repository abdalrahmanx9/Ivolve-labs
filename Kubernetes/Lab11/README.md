# Lab 11 — Namespace and Resource Quota

## Namespace + quota

```bash
kubectl create namespace ivolve
kubectl apply -f resourcequota.yaml
```

`resourcequota.yaml`:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ivolve-quota
  namespace: ivolve
spec:
  hard:
    pods: "3"
```

Note: the sheet's `ivolveQuota` name can't be used as-is — Kubernetes resource names must be lowercase RFC 1123 (`ivolve-quota`).

## Verify the limit

Created pods 1–3 fine, the 4th was rejected:

```
$ kubectl run quota-test-4 -n ivolve ...
Error from server (Forbidden): pods "quota-test-4" is forbidden:
exceeded quota: ivolve-quota, requested: pods=1, used: pods=3, limited: pods=3

$ kubectl get resourcequota -n ivolve
NAME           REQUEST   LIMIT
ivolve-quota   pods: 3/3
```

Test pods deleted after verification; quota remains enforced on the namespace.
