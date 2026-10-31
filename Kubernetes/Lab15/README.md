# Lab 15 — Node.js Deployment with ClusterIP Service

Deploying the app image from Lab 8 (abdalrahmanx/ivolve-app:v1) into the `ivolve` namespace, 2 replicas. Manifest in `deployment.yaml`, plus a ClusterIP service `ivolve-app-svc` on port 3000 in front of it.

The app wants MySQL to exist before it starts, so the pod has an init container (also `mysql:8.0`) that connects to the database first and sets up the database and user:

```sql
CREATE DATABASE IF NOT EXISTS ivolve;
CREATE USER IF NOT EXISTS 'ivolve'@'%' IDENTIFIED BY 'ivolvedb123';
GRANT ALL PRIVILEGES ON ivolve.* TO 'ivolve'@'%';
FLUSH PRIVILEGES;
```

It reads the connection details from the same ConfigMap and Secret the app uses (envFrom), so nothing is duplicated.

The pod spec also carries the node selector `project=ivolve` and the toleration from Lab 10, so both replicas land on `desktop-worker`, and the PVC from Lab 13 is mounted at `/app/logs` where the app writes its access log.

One fix I had to make first: the Lab 12 ConfigMap had `DB_HOST: mysql.ivolve.svc.cluster.local`, but the headless service from Lab 14 is actually named `ivolve-db-svc` — the app could never have resolved that hostname. Updated the ConfigMap to `ivolve-db-svc.ivolve.svc.cluster.local`.

## Checking it works

Both replicas on the right node:

```
ivolve-app-5d4c4c8d8c-mmnlm   Running   desktop-worker
ivolve-app-5d4c4c8d8c-ndtz4   Running   desktop-worker
```

The init container did its job (checked from the MySQL pod):

```
$ mysql -uroot -p... -e "SHOW GRANTS FOR 'ivolve'@'%';"
GRANT USAGE ON *.* TO `ivolve`@`%`
GRANT ALL PRIVILEGES ON `ivolve`.* TO `ivolve`@`%`
```

App logs:

```
Attempting to connect to MySQL...
Connected to MySQL and 'ivolve' DB found.
Server started on http://0.0.0.0:3000
```

And through the service. I couldn't create a throwaway curl pod because the Lab 11 quota is full (2 app pods + mysql), so I exec'd into one of the app pods instead:

```
$ kubectl exec deployment/ivolve-app -n ivolve -- wget -qO- http://ivolve-app-svc:3000/health
iVolve web app is working! Keep calm and code on!
```
