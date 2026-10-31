# Lab 16 — Resource Requests and Limits

Added this to the app container in the Lab 15 deployment:

```yaml
resources:
  requests:
    cpu: "1"
    memory: 1Gi
  limits:
    cpu: "2"
    memory: 2Gi
```

Applying it didn't work on the first try. A rolling update starts the new pod before killing the old one, and the namespace quota from Lab 11 was already full (2 app pods + MySQL = 3 of 3), so the surge pod got rejected:

```
FailedCreate: pods "..." is forbidden: exceeded quota: ivolve-quota,
requested: pods=1, used: pods=3, limited: pods=3
```

Raised the quota to 5 in `Lab11/resourcequota.yaml` and the rollout completed. The quota still does its job, it just has headroom now.

## describe

```
Limits:
  cpu:     2
  memory:  2Gi
Requests:
  cpu:     1
  memory:  1Gi
```

## kubectl top

The metrics API wasn't there — Docker Desktop's kind cluster ships without metrics-server — so I downloaded components.yaml and added `--kubelet-insecure-tls` for kind's self-signed certs:

```bash
curl -LO https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
sed -i '/--kubelet-preferred-address-types/a \        - --kubelet-insecure-tls' components.yaml
kubectl apply -f components.yaml
```

```
$ kubectl top pod -n ivolve
NAME                          CPU(cores)   MEMORY(bytes)
ivolve-app-5d4c4c8d8c-mmnlm   0m           20Mi
ivolve-app-5d4c4c8d8c-ndtz4   0m           21Mi
ivolve-db-0                   7m           365Mi
```

The app pods idle at ~20Mi while their request is 1Gi — requests are what the scheduler reserves, not what the pod actually uses.
