# Base image: Official LTS Jenkins controller with Java 17 runtime
FROM jenkins/jenkins:lts-jdk17

# Elevate privileges to root to install system CLI tools:
USER root

# Install build tools and CLIs (Maven, curl, gnupg, kubectl, and docker CLI):
#   apt-get update                  : Refreshes local package indexes
#   -y                              : Automatically confirms installation prompts
#   --no-install-recommends         : Skips optional/recommended packages to reduce image size
#   rm -rf /var/lib/apt/lists/*     : Removes apt package cache to keep layer small
#   curl -fsSL:
#     -f / --fail                   : Fail silently on HTTP errors (return non-zero exit code)
#     -s / --silent                 : Silent/quiet mode, hides progress bar
#     -S / --show-error             : Show error message if curl fails despite -s
#     -L / --location               : Follow HTTP redirects
#   chmod +x                        : Adds executable permissions to downloaded binary
#   tar -xz:
#     -x                            : Extract archive
#     -z                            : Decompress via gzip
#     --strip-components=1          : Strip top-level directory inside tarball so binary lands directly in destination
#     -C /usr/local/bin             : Target destination folder for extracted files
RUN apt-get update && apt-get install -y --no-install-recommends \
      maven curl gnupg \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL "https://dl.k8s.io/release/v1.33.13/bin/linux/amd64/kubectl" \
       -o /usr/local/bin/kubectl && chmod +x /usr/local/bin/kubectl \
    && curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-27.5.1.tgz \
       | tar -xz --strip-components=1 -C /usr/local/bin docker/docker

# Install Trivy security vulnerability scanner:
#   gpg --dearmor -o:
#     --dearmor                     : Converts ASCII-armored GPG public key into binary keyring format
#     -o <file>                     : Specifies destination path for keyring file
RUN curl -fsSL https://aquasecurity.github.io/trivy-repo/deb/public.key \
      | gpg --dearmor -o /usr/share/keyrings/trivy.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" \
       > /etc/apt/sources.list.d/trivy.list \
    && apt-get update && apt-get install -y --no-install-recommends trivy \
    && rm -rf /var/lib/apt/lists/*

# Pre-install essential Jenkins plugins at build time:
#   --plugins <list>                : Installs specified plugins and their dependencies
RUN jenkins-plugin-cli --plugins workflow-aggregator git docker-workflow pipeline-stage-view matrix-auth plain-credentials

# Copy Configuration as Code Groovy scripts executed automatically upon Jenkins startup:
COPY init.groovy.d/ /usr/share/jenkins/ref/init.groovy.d/

# Drop back to non-root least-privilege user for security:
USER jenkins
