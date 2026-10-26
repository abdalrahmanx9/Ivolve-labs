# Lab 13 — Persistent Storage (PV + PVC)

`pv-pvc.yaml` — one manifest, two objects:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: ivolve-pv
spec:
  capacity:
    storage: 1Gi
  accessModes: ["ReadWriteMany"]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ""                 # <- no StorageClass: static binding only
  hostPath:
    path: /mnt/app-logs
    type: DirectoryOrCreate
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ivolve-pvc
  namespace: ivolve
spec:
  accessModes: ["ReadWriteMany"]
  storageClassName: ""                 # must match the PV
  resources:
    requests:
      storage: 1Gi
```

A couple of things that are easy to get wrong here:

- `storageClassName: ""` has to be set on both. Leave it out and the PVC ignores the manual PV and gets dynamically provisioned by the cluster's default StorageClass instead — the empty string is what forces the static bind to `ivolve-pv`.
- PVC names must be lowercase (`ivolve-pvc`, not `ivolvePVC`) — same RFC 1123 rule as Lab 11.

## Verify

```
$ kubectl get pv,pvc -n ivolve
NAME            CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM
ivolve-pv       1Gi        RWX            Retain           Bound    ivolve/ivolve-pvc

NAME          STATUS   VOLUME      CAPACITY   ACCESS MODES
ivolve-pvc    Bound    ivolve-pv   1Gi        RWX
```
