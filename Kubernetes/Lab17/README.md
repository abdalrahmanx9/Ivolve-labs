# Lab 17 — NetworkPolicy

Goal: only the application pods may talk to MySQL, and only on port 3306. Manifest in `networkpolicy.yaml`:

```yaml
spec:
  podSelector:
    matchLabels:
      app: ivolve-db        # applies to the MySQL pod
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: ivolve-app
      ports:
        - protocol: TCP
          port: 3306
```

Applied:

```
$ kubectl get networkpolicy -n ivolve
NAME        POD-SELECTOR   AGE
ivolve-np   app=ivolve-db   1s
```

With this in place, pods labeled `app=ivolve-app` in the `ivolve` namespace can open TCP 3306 to MySQL; anything else (other namespaces, unlabeled pods) gets dropped.

One honest note: Docker Desktop's kind cluster uses the kindnet CNI, which doesn't actually enforce NetworkPolicies — the object is accepted and correct, but traffic isn't filtered here. I can't demo the blocking on this cluster. On a CNI that supports it (Calico, Cilium — like the kubeadm cluster in Lab 9) the same manifest works, and you'd see a `nc -zv` from a non-allowed pod time out.
