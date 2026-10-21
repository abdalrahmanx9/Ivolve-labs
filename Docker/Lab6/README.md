# Lab 6 — Environment Variables and Resource Management

App: Flask, reads `APP_NAME`/`APP_ENV` from the environment and refuses to start without them. Port 5000.

`PythonApp/Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

Note: something else on this machine already owns host port 5000, so containers publish on 5001/5002/5003 → 5000. Container port is still 5000.

## 1. Build + run with `-e` flags and resource limits

```bash
docker build -t ivolve1 .
docker run -d --name container1 -p 5001:5000 \
  -e APP_NAME=iVolveApp1 -e APP_ENV=stg \
  --cpus 1 --memory 256m ivolve1
```

Verify:

```
$ curl http://localhost:5001/
{"application":"iVolveApp1","environment":"stg","message":"Welcome to the Docker Env & Resource Management Lab!"}

$ docker exec container1 env | grep APP
APP_NAME=iVolveApp1
APP_ENV=stg

$ docker inspect container1 --format 'CPUs={{.HostConfig.NanoCpus}} Memory={{.HostConfig.Memory}}'
limits: CPUs=1000000000 Memory=268435456

$ docker stats --no-stream container1
container1: CPU=0.01% MEM=24.05MiB / 256MiB
```

## 2. Run with `--env-file`

`env.txt`:

```
APP_NAME=iVolveApp2
APP_ENV=prod
```

```bash
docker run -d --name container2 -p 5002:5000 --env-file env.txt ivolve1
curl http://localhost:5002/
{"application":"iVolveApp2","environment":"prod",...}
```

## 3. Env vars baked into the image

`PythonApp/Dockerfile.env`:

```dockerfile
FROM ivolve1
ENV APP_NAME=iVolveApp3
ENV APP_ENV=dev
CMD ["python", "app.py"]
```

```bash
docker build -t ivolve3 -f Dockerfile.env .
docker run -d --name container3 -p 5003:5000 ivolve3
curl http://localhost:5003/
{"application":"iVolveApp3","environment":"dev",...}

$ docker exec container3 env | grep APP
APP_NAME=iVolveApp3
APP_ENV=dev
```

## Three ways to set env, compared

| Way | Scope | Best for |
|---|---|---|
| `-e` flags | one container | one-off overrides, secrets |
| `--env-file` | one container | many vars, per-environment config files |
| `ENV` in Dockerfile | every container from the image | defaults that rarely change |

Cleanup: `docker rm -f container1 container2 container3`
