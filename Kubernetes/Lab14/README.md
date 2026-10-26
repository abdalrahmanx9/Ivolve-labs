# Lab 14 — MySQL StatefulSet with Headless Service

`statefulset.yaml` — headless Service + StatefulSet in the `ivolve` namespace:

- 1 replica of `mysql:8.0`
- **envFrom** pulls `ivolve-cm` (ConfigMap) and `ivolve-secret` (Secret) from Lab 12 — `DB_HOST`, `DB_USER`, `MYSQL_ROOT_PASSWORD`, `DB_PASSWORD` become container env vars
- `nodeSelector: project=ivolve` + toleration for `workload=ivolveApp:NoSchedule` (Lab 10) — pod lands on the isolated node
- `volumeClaimTemplates` mounts 1Gi at `/var/lib/mysql` (dynamically provisioned by the cluster's default StorageClass)
- Service is **headless** (`clusterIP: None`) so the pod gets a stable DNS name

```bash
kubectl apply -f statefulset.yaml
kubectl wait --for=condition=Ready pod/ivolve-db-0 -n ivolve --timeout=180s
```

## Verify: pod placement

```
$ kubectl get pods -n ivolve -o wide
NAME          READY   STATUS    NODE
ivolve-db-0   1/1     Running   desktop-worker    <- the tainted+labeled node
```

## Verify: database operational

```
$ kubectl exec ivolve-db-0 -n ivolve -- \
    mysql -uroot -p<password> -e "SHOW DATABASES;"
Database
information_schema
ivolve          <- created via MYSQL_DATABASE env
mysql
performance_schema
sys
```

## Verify: DNS inside the cluster

Headless service and per-pod FQDN both resolve:

```
$ nslookup ivolve-db-svc.ivolve.svc.cluster.local
Address: 10.244.2.3

$ nslookup ivolve-db-0.ivolve-db-svc.ivolve.svc.cluster.local
Address: 10.244.2.3
```

And a real connection through the resolved name:

```
$ kubectl exec ivolve-db-0 -n ivolve -- \
    mysql -h ivolve-db-0.ivolve-db-svc.ivolve.svc.cluster.local -uroot -p... \
    -e "SHOW DATABASES; SELECT @@hostname;"
ivolve
@@hostname
ivolve-db-0
```

Note: the StatefulSet is `ivolve-db` (lowercase, per RFC 1123), so the pod is `ivolve-db-0`.
