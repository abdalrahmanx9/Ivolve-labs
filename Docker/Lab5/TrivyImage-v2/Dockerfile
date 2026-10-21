# Base image: Modern Node.js 22 LTS on lightweight Alpine Linux (minimal attack surface)
FROM node:22-alpine

# Set application working directory:
WORKDIR /app

# Copy dependency definition first to leverage Docker layer caching:
COPY package.json ./

# Install production dependencies and harden the image against vulnerabilities:
#   --omit=dev       : Skips development dependencies (testing frameworks, linters) to reduce CVE exposure
#   cache clean --force: Purges npm cache to reclaim layer disk space
#   rm -rf ...       : Removes npm and npx CLIs from runtime image so package managers cannot be exploited in production
RUN npm install --omit=dev \
    && npm cache clean --force \
    && rm -rf /usr/local/lib/node_modules /usr/local/bin/npm /usr/local/bin/npx

# Copy application source code:
COPY app.js ./

# Document expected service port:
EXPOSE 3000

# JSON exec form starts Node.js application directly as PID 1:
CMD ["node", "app.js"]
