# Lab 12 — ConfigMap and Secret

In the `ivolve` namespace (from Lab 11).

## ConfigMap — non-sensitive MySQL config

`configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ivolve-cm
  namespace: ivolve
data:
  DB_HOST: "mysql.ivolve.svc.cluster.local"   # MySQL StatefulSet headless Service
  DB_USER: "ivolve"
```

## Secret — sensitive credentials, Base64-encoded in the manifest

`secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ivolve-secret
  namespace: ivolve
type: Opaque
data:
  MYSQL_ROOT_PASSWORD: "aXZvbHZlcm9vdDEyMw=="   # base64("ivolveroot123")
  DB_PASSWORD: "aXZvbHZlZGIxMjM="               # base64("ivolvedb123")
```

(`data` values must be Base64 — encode with `echo -n 'value' | base64`.)

## Verify

```
$ kubectl get configmap,secret -n ivolve
NAME                   DATA
configmap/ivolve-cm    2

NAME                   TYPE
secret/ivolve-secret   Opaque

$ kubectl get secret ivolve-secret -n ivolve -o jsonpath='{.data.MYSQL_ROOT_PASSWORD}' | base64 -d
ivolveroot123
```

Note: resource names had to be lowercase (`ivolve-cm`/`ivolve-secret`) — same RFC 1123 rule as Lab 11.
