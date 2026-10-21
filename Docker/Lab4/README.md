# Lab 4 — Image Optimization and Export/Load

App: Spring Boot demo (`ImageOptimization-` repo), served on port 8080.

## 1. Baseline image (existing Dockerfile)

The repo's Dockerfile builds in a single stage from `maven:3.9.15-eclipse-temurin-17-alpine` — JDK + Maven + source + `~/.m2` all end up in the final image, running as root.

```bash
docker build -t image1 .        # image1  420MB
docker run -d --name container1 -p 8080:8080 image1
curl http://localhost:8080/     # -> Hello from Dockerized Spring Boot!
docker stop container1 && docker rm container1
```

## 2. Multi-stage + non-root (`Dockerfile.optimized`)

```dockerfile
FROM maven:3.9.15-eclipse-temurin-17-alpine AS build
WORKDIR /app
COPY . .
RUN mvn package -B

FROM eclipse-temurin:17-jre-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=build --chown=app:app /app/target/demo-0.0.1-SNAPSHOT.jar app.jar
USER app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Build stage has the full toolchain; final stage keeps only the JRE and the jar. Alpine useradd syntax (`addgroup -S` / `adduser -S`) since the runtime is alpine.

```bash
docker build -t image2 -f Dockerfile.optimized .    # image2  210MB
docker run -d --name container2 -p 8080:8080 image2
curl http://localhost:8080/          # -> Hello from Dockerized Spring Boot!
docker exec container2 whoami        # -> app
docker stop container2 && docker rm container2
```

## Size comparison

| Image | Base | Size |
|---|---|---|
| image1 | maven + JDK (single stage) | 420 MB |
| image2 | JRE only (multi-stage, non-root) | **210 MB** |

Half the size: build tools, source, and Maven's dependency cache never make it into the runtime layer.

## Export / load

```bash
docker save image2 -o lab-image.tar     # 201 MB tar
docker rmi image2
docker load -i lab-image.tar            # Loaded image: image2:latest
docker images image2                    # image2  210MB — restored
```

`docker save`/`load` moves images between hosts with no registry. (The lab sheet's "image2.tar" and "lab-image.tar" are the same file — used lab-image.tar.)
