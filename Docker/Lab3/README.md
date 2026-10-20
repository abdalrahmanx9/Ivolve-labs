# Lab 3 — Docker Image for a Java Application

Two ways to containerize the same Maven calculator app:

- **Part 1** — build inside Docker (source copied in, `mvn package` runs in the image)
- **Part 2** — build locally, copy only the jar into a JRE image

Source is vendored in `part1/CalculatorMavenApp/` (includes its Dockerfile), the locally-built jar sits in `part2/`.

## Part 1 — Build Inside Docker

`part1/CalculatorMavenApp/Dockerfile`:

```dockerfile
FROM maven:3.9-eclipse-temurin-17

RUN groupadd -r app && useradd -rm -g app app

WORKDIR /app
RUN chown app:app /app

COPY --chown=app:app . .

USER app

RUN mvn package -B

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "target/calculator.jar"]
```

Build, run, verify, clean up:

```bash
docker build -t app1 .           # -> app1  534MB
echo "10 3" | docker run -i --name container1 app1
docker rm container1 && docker rmi app1
```

Output:

```
Enter first number: Enter second number: a = 10.0, b = 3.0
Sum: 13.0
Subtract: 7.0
Multiply: 30.0
Divide: 3.3333333333333335
```

## Part 2 — Build Locally

Jar built on the host (Lab 1: `mvn package` → `target/calculator.jar`, 3.7 KB), copied to `part2/`.

`part2/Dockerfile`:

```dockerfile
FROM eclipse-temurin:17-jre

RUN groupadd -r app && useradd -rm -g app app

WORKDIR /app

COPY --chown=app:app calculator.jar .

USER app

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "calculator.jar"]
```

```bash
docker build -t app2 .           # -> app2  296MB
echo "10 3" | docker run -i --name container2 app2
docker rm container2 && docker rmi app2
```

Same correct output as Part 1.

## Bonus — Size Comparison

| Image | Base | Size |
|---|---|---|
| app1 | `maven:3.9-eclipse-temurin-17` (JDK + Maven) | **534 MB** |
| app2 | `eclipse-temurin:17-jre` (runtime only) | **296 MB** |

- app1 carries the full JDK, Maven itself, the source code, and every dependency Maven downloaded (~/.m2) in its layers — none of that is needed at runtime.
- app2 carries only the JRE and the 3.7 KB jar. Build tools stay on the build machine, where they belong.
- app1's advantage: no Java/Maven install needed to build it — Docker is the only requirement. app2 needs a working local toolchain.

Real-world best of both: a **multi-stage build** — build in the Maven image, copy just the jar to a JRE image (`--from=build`), getting ~296 MB with zero local tooling.
