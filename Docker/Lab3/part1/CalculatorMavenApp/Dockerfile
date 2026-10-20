FROM maven:3.9-eclipse-temurin-17

RUN groupadd -r app && useradd -rm -g app app

WORKDIR /app

RUN chown app:app /app

COPY --chown=app:app . .

USER app

RUN mvn package -B

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "target/calculator.jar"]
