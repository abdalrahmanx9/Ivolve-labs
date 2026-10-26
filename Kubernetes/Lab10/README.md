# Lab 10 — Node Isolation with Taints and Labels

Cluster: local Docker Desktop Kubernetes (3 nodes). Target node: `desktop-worker`.

## Taint + label

```bash
kubectl taint node desktop-worker workload=ivolveApp:NoSchedule
kubectl label node desktop-worker project=ivolve
```

## Verify

```
$ kubectl describe node desktop-worker | grep -A1 Taints
Taints:             workload=ivolveApp:NoSchedule

$ kubectl get nodes --show-labels | grep ivolve
desktop-worker   Ready   ...   project=ivolve
```

## Proof of isolation

Two test pods (`allowed-pod.yaml` has the toleration + `nodeSelector: project=ivolve`, `blocked-pod.yaml` has neither):

```
$ kubectl get pods -o custom-columns=NAME:.metadata.name,PHASE:.status.phase,NODE:.spec.nodeName
NAME          PHASE     NODE
allowed-pod   Running   desktop-worker     <- toleration + label match
blocked-pod   Running   desktop-worker2    <- no toleration, pushed to another node
```

- A pod **without** the toleration can never land on `desktop-worker` (NoSchedule).
- A pod **with** the toleration *and* the `project=ivolve` selector targets exactly that node.

Cleanup: `kubectl delete pod blocked-pod allowed-pod` (taint and label stay on the node).
