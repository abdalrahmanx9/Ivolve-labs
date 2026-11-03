# Lab 18 — Monitoring with Prometheus, Grafana, and node-exporter

All in a new `monitoring` namespace, plain manifests, no Helm.

## node-exporter DaemonSet

`01-node-exporter.yaml` runs `prom/node-exporter:v1.8.1` with hostNetwork and hostPID, `/proc`, `/sys` and `/` mounted read-only from the host, and a toleration for everything so it also lands on the control plane node:

```
$ kubectl get pods -n monitoring -o wide
node-exporter-4j5wx   Running   desktop-control-plane   172.22.0.5
node-exporter-6pzhb   Running   desktop-worker2         172.22.0.6
node-exporter-jnzv2   Running   desktop-worker          172.22.0.4
```

One per node, and because of hostNetwork each pod holds the node's own IP.

(Small mistake on the way: I first used `prometheus/node-exporter` as the image name — that doesn't exist, the real one is `prom/node-exporter`. Three ImagePullBackOffs before I noticed.)

## Metrics on the node

From a pod in the cluster, `http://<node_IP>:9100/metrics` serves the exporter:

```
$ wget -qO- http://172.22.0.4:9100/metrics | head
# HELP go_gc_duration_seconds A summary of the pause duration...
go_gc_duration_seconds{quantile="0"} 1.8886e-05
```

## Prometheus

`02-prometheus.yaml` — config in a ConfigMap, one replica, plus RBAC (a small ClusterRole to list nodes) because the scrape config uses kubernetes service discovery:

```yaml
- job_name: node-exporter
  kubernetes_sd_configs:
    - role: node
  relabel_configs:
    - source_labels: [__address__]
      regex: "(.*):10250"
      replacement: "${1}:9100"
      target_label: __address__
```

That trick discovers nodes via the API (address :10250) and rewrites the port to 9100, so it survives node IP changes. The config also points alerting at `alertmanager:9093`.

Checking the targets API, all three nodes are being scraped:

```
scrapeUrl: http://172.22.0.4:9100/metrics  health: "up"
scrapeUrl: http://172.22.0.5:9100/metrics  health: "up"
scrapeUrl: http://172.22.0.6:9100/metrics  health: "up"
```

## Alertmanager

`03-alertmanager.yaml` — one replica with a minimal config (a default webhook receiver). Prometheus is already wired to it in its config; without alert rules it just sits there, which is all this lab needs.

## Grafana

`04-grafana.yaml` — deployment + service, with the datasource (Prometheus) and a dashboard provider provisioned via ConfigMaps so there's no clicking in the UI. For the dashboard itself I used the well-known "Node Exporter Full" dashboard (id 1860) — downloaded its JSON into this folder (`node-exporter-full.json`) and loaded it as a ConfigMap, because provisioning can't fetch dashboards by id on its own:

```bash
kubectl apply -f 00-namespace-rbac.yaml -f 01-node-exporter.yaml -f 02-prometheus.yaml -f 03-alertmanager.yaml -f 04-grafana.yaml
kubectl create configmap grafana-dashboard-k8s -n monitoring --from-file=node-exporter-full.json
kubectl rollout restart deployment/grafana -n monitoring
```

Health check from inside:

```
$ wget -qO- http://grafana:3000/api/health
{"database": "ok", "version": "11.1.0"}
```

To actually look at the dashboard: `kubectl port-forward -n monitoring svc/grafana 3000:3000`, then http://localhost:3000 (admin/admin) — the Node Exporter Full dashboard is in the Kubernetes folder, one graph per node from the Prometheus data.
