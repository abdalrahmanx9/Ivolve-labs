# Base image: Official Maven 3.9 image packaged with Eclipse Temurin OpenJDK 17
FROM maven:3.9-eclipse-temurin-17

# Create an unprivileged system user and group for security:
#   groupadd -r app   : -r creates a system group (low GID, no password aging)
#   useradd -rm -g app: -r creates a system user (low UID)
#                       -m forces creation of home directory (/home/app)
#                       -g app sets primary group to 'app'
RUN groupadd -r app && useradd -rm -g app app

# Set execution workspace inside the container
WORKDIR /app

# Ensure non-root user owns the working directory
RUN chown app:app /app

# Copy application source code into the container image:
#   --chown=app:app : Directly sets file ownership on copy, preventing an extra RUN chown layer
COPY --chown=app:app . .

# Drop root privileges and switch runtime context to non-root user
USER app

# Compile and package the Java application:
#   -B : Batch / Non-Interactive mode (silences progress bars and disables interactive prompts)
RUN mvn package -B

# Document network port listening inside container (informational metadata)
EXPOSE 8080

# Configure default container executable using preferred JSON Exec format:
#   java -jar target/calculator.jar : Launches the built executable JAR
ENTRYPOINT ["java", "-jar", "target/calculator.jar"]
