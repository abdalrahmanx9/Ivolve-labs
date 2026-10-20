FROM eclipse-temurin:17-jre

RUN groupadd -r app && useradd -rm -g app app

WORKDIR /app

COPY --chown=app:app calculator.jar .

USER app

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "calculator.jar"]
