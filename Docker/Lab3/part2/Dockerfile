# Base image: Lightweight Java Runtime Environment (JRE 17) only — avoids heavy JDK/compiler tools
FROM eclipse-temurin:17-jre

# Create dedicated non-root application user for least-privilege security:
#   groupadd -r app   : -r creates a system group (low GID)
#   useradd -rm -g app: -r creates a system user (low UID)
#                       -m creates home directory (/home/app)
#                       -g app assigns primary group 'app'
RUN groupadd -r app && useradd -rm -g app app

# Establish working directory
WORKDIR /app

# Copy ONLY the pre-compiled JAR artifact from the host build:
#   --chown=app:app : Sets ownership directly on copy to avoid extra intermediate filesystem layers
COPY --chown=app:app calculator.jar .

# Switch execution security context from root to unprivileged 'app' user
USER app

# Document listener port for application container
EXPOSE 8080

# Run application using JSON array Exec syntax (signals like SIGTERM pass directly to Java process)
ENTRYPOINT ["java", "-jar", "calculator.jar"]
