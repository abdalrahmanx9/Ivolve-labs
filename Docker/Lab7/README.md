# Lab 7 — Multi-Network Microservices, Volumes, and Bind Mounts

Three Flask services from `MicroserviceApp/` (Dockerfiles included in the repo):

| Service | Port | Talks to |
|---|---|---|
| frontend | 3000 (published on 8080) | `BACKEND_URL` (default `http://backend:5000`) |
| backend | 5000 | `NOTIFICATION_URL` (default `http://notification:5001/notify`) |
| notification | 5001 | — |

Backend persists messages in `/app/data` and logs to `/app/logs`; notification logs to `/app/logs`.

## 1. Build images

```bash
docker build -t frontend frontend
docker build -t backend backend
docker build -t notification notification
```

## 2. Networks with separate subnets

```bash
docker network create --driver bridge --subnet 172.30.0.0/24 frontend-backend
docker network create --driver bridge --subnet 172.31.0.0/24 backend-notification
```

## 3. Volumes + host bind mount

```bash
docker volume create backend-logs
docker volume create notification-logs
mkdir backend-data        # host dir for backend's /app/data (bind mount)
```

## 4. Run — backend joins both networks

```bash
docker run -d --name notification --network backend-notification \
  -v notification-logs:/app/logs notification

docker run -d --name backend --network backend-notification \
  -v backend-logs:/app/logs \
  -v ./backend-data:/app/data \
  -e NOTIFICATION_URL=http://notification:5001/notify backend

docker network connect frontend-backend backend   # second network

docker run -d --name frontend --network frontend-backend \
  -p 8080:3000 -e BACKEND_URL=http://backend:5000 frontend
```

## 5. Verify

```
$ curl http://localhost:8080/            -> page renders, no "backend unavailable" error
$ curl -X POST -d "message=hello from lab 7" http://localhost:8080/send
$ curl http://localhost:8080/            -> <li>hello from lab 7</li>
```

Persistence proof — messages survive in the bind mount, logs in the volumes:

```
$ cat backend-data/messages.json
["hello from lab 7"]

$ docker exec backend tail -1 /app/logs/backend.log
... INFO 172.30.0.3 ... "GET /messages" 200 -        <- frontend, 172.30.x net

$ docker exec notification tail -1 /app/logs/notification.log
... INFO 172.31.0.3 ... "POST /notify" 200 -         <- backend, 172.31.x net
```

The log lines prove the network split: frontend reaches backend over `frontend-backend` (172.30.0.0/24), backend reaches notification over `backend-notification` (172.31.0.0/24) — and notification has no route to the frontend at all.

Teardown: `docker rm -f frontend backend notification && docker network rm frontend-backend backend-notification && docker volume rm backend-logs notification-logs`
