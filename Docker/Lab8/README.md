# Lab 8 — Node.js + MySQL Stack with Docker Compose

`iVolveApp/`: Express app on port 3000 that needs MySQL env vars (`DB_HOST`, `DB_USER`, `DB_PASSWORD`) and an existing `ivolve` database before it will serve.

## docker-compose.yml

- **app** — built from the repo Dockerfile, port 3000, DB env vars, logs volume at `/app/logs`
- **db** — `mysql:8.0` with `MYSQL_DATABASE=ivolve` (creates the DB the app waits for), data in `db_data` volume at `/var/lib/mysql`
- **network** — `ivolve-net` (named explicitly so compose doesn't prefix it)
- **volumes** — `app_logs`, `db_data`

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      DB_HOST: db
      DB_USER: ivolve
      DB_PASSWORD: ivolve123
      DB_NAME: ivolve
    volumes:
      - app_logs:/app/logs
    depends_on:
      - db
    networks:
      - ivolve-net

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: ivolve
      MYSQL_USER: ivolve
      MYSQL_PASSWORD: ivolve123
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - ivolve-net

networks:
  ivolve-net:
    name: ivolve-net

volumes:
  app_logs:
  db_data:
```

## Start and verify

```bash
docker compose up -d --build
curl http://localhost:3000/health
```

```
iVolve web app is working! Keep calm and code on!   [HTTP 200]
```

Everything in place:

```
$ docker compose exec app ls /app/logs        -> access.log   (app_logs volume)
$ docker volume ls                            -> ivolveapp_app_logs, ivolveapp_db_data
$ docker network ls                           -> ivolve-net
$ docker compose exec db sh -c "echo 'SHOW DATABASES;' | mysql -uivolve -pivolve123"
Database
ivolve
```

## Push to Docker Hub

```bash
docker tag ivolveapp-app abdalrahmanx/ivolve-app:v1
docker push abdalrahmanx/ivolve-app:v1
```

```
v1: digest: sha256:23d090e3d72bfb467300dc59845170626c47cae6a0cceed645150b18f714a680
```

Live at https://hub.docker.com/r/abdalrahmanx/ivolve-app

Teardown: `docker compose down` (add `-v` to also drop the volumes).
