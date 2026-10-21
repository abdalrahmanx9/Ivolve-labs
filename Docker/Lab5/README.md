# Lab 5 — Vulnerability Scanning with Trivy

App: tiny Express app on `node:18-bullseye` with `express 4.18.2` — deliberately outdated.

## 1. Build and scan v1

```bash
docker build -t trivy-lab:v1 .     # 1GB
```

Install Trivy (0.76.1 here): binary from https://github.com/aquasecurity/trivy/releases, or `apt install trivy` / `brew install trivy`.

```bash
trivy image trivy-lab:v1
trivy image --severity HIGH,CRITICAL trivy-lab:v1
```

```
Total: 2269 (HIGH: 2048, CRITICAL: 221)
```

Almost all from Debian bullseye packages (bash, curl, imagemagick...) — the base image is ~4 years past its prime.

HTML report:

```bash
trivy image --format template --template "@contrib/html.tpl" -o report-v1.html trivy-lab:v1
```

## 2. Bonus — remediation (`TrivyImage-v2/`)

Two changes:

```dockerfile
FROM node:22-alpine          # was node:18-bullseye
```

```json
"express": "^4.21.2"          // was 4.18.2
```

First attempt with `node:22-slim` still left 68 findings, and 11 remained on alpine — all in **npm's own bundled toolchain** (`pacote`, `sigstore`, `brace-expansion`...) shipped inside the base image, not in app dependencies. A production image doesn't need a package manager, so the final Dockerfile strips npm after installing:

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev \
    && npm cache clean --force \
    && rm -rf /usr/local/lib/node_modules /usr/local/bin/npm /usr/local/bin/npx
COPY app.js ./
EXPOSE 3000
CMD ["node", "app.js"]
```

```bash
docker build -t ivolve-app:v2 .    # 172MB
trivy image --severity HIGH,CRITICAL --exit-code 1 ivolve-app:v2   # exit 0
```

| Image | Size | HIGH/CRITICAL |
|---|---|---|
| trivy-lab:v1 | 1 GB | 2269 |
| ivolve-app:v2 | 172 MB | **0** |

Still works:

```
$ curl http://localhost:3000/
Welcome to the Trivy Security Lab!
```

New report: `trivy image --format template --template "@contrib/html.tpl" -o report-v2.html ivolve-app:v2`

(Reports aren't committed — v1 is 40 MB of findings; regenerate with the commands above.)
