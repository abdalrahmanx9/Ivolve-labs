# generator/module2_docker.py

LABS_MODULE_2 = [
    {
        "id": "lab-3",
        "number": "Lab 03",
        "title": "Creating a Docker Image for a Java Application",
        "module": "Docker",
        "icon": "🐳",
        "tags": ["Docker", "Java 17", "Image Layers", "Non-Root User"],
        "summary": "Learn the two ways to put a Java app into Docker: building inside the container vs building on your host machine.",
        "question": [
            "Clone the application code: https://github.com/Ibrahim-Adel15/CalculatorMavenApp.git",
            "Part 1: Build Inside Docker",
            "  • Write a Dockerfile using a Maven image with Java 17.",
            "  • Create a working directory and a non-root user.",
            "  • Copy the source code and build the application using mvn package.",
            "  • Run the generated JAR file and expose port 8080.",
            "  • Build an image named app1 and note its size.",
            "  • Run container1, verify the application, then delete the container and image.",
            "Part 2: Build Locally",
            "  • Build the application locally using Maven.",
            "  • Write a Dockerfile using a Java 17 runtime image.",
            "  • Create a working directory and a non-root user.",
            "  • Copy the generated JAR file into the image and expose port 8080.",
            "  • Build an image named app2 and note its size.",
            "  • Run container2, verify the application, then delete the container and image.",
            "Bonus: Compare the image sizes and explain the differences between the two approaches."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Imagine you want to give your Java calculator to a friend to run on their computer. You have two choices:</p>
            <ul>
                <li><strong>Choice A (Build Inside Docker):</strong> You give your friend the raw source code and tell Docker to download Maven, compile the code, and run it.
                    <br><em>The Good:</em> Your friend does not need Java or Maven installed on their laptop—Docker does everything.
                    <br><em>The Bad:</em> The final Docker image is huge (<strong>534 MB</strong>) because it has to carry the compiler, Maven tools, source files, and temporary caches that you never need when just running the app.</li>
                <li><strong>Choice B (Build Locally):</strong> You compile the code on your own laptop first using <code>mvn package</code> to make a tiny 3.7 KB <code>calculator.jar</code> file. Then you give Docker just that JAR file and a lightweight Java runtime (JRE).
                    <br><em>The Good:</em> The image is almost half the size (<strong>296 MB</strong>), starts faster, and is much more secure.
                    <br><em>The Bad:</em> Whoever builds the image must have Maven and Java installed on their machine first.</li>
                <li><strong>Why Non-Root User?</strong> By default, Docker runs everything as the <code>root</code> user (the super administrator). If a hacker finds a bug in your app, they might take over the entire host machine. Creating a simple unprivileged user named <code>app</code> stops this.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-comparison">
                <div class="comparison-card">
                    <div class="comp-badge">Part 1: Build Inside Docker</div>
                    <div class="comp-flow">
                        <span>Source Code</span> ➔ <span>Maven Image (JDK)</span> ➔ <span>mvn package</span>
                    </div>
                    <div class="comp-metric danger">Size: 534 MB (Heavy)</div>
                    <div class="comp-note">Carries Maven tools, source code, and cached dependencies.</div>
                </div>
                <div class="comparison-card">
                    <div class="comp-badge success">Part 2: Build Locally</div>
                    <div class="comp-flow">
                        <span>Pre-built JAR (3.7 KB)</span> ➔ <span>JRE Runtime Image</span> ➔ <span>java -jar</span>
                    </div>
                    <div class="comp-metric success">Size: 296 MB (Slim)</div>
                    <div class="comp-note">Contains only Java runtime and the compiled JAR file.</div>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>Part 1: Build Inside Docker (<code>app1</code>)</h5>
            <p>Click below to inspect the actual Dockerfile in your workspace:</p>
            <div class="file-links-bar">
                <a href="Docker/Lab3/part1/CalculatorMavenApp/Dockerfile" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab3/part1/CalculatorMavenApp/Dockerfile</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-dockerfile"># Base image: Official Maven 3.9 image packaged with Eclipse Temurin OpenJDK 17
FROM maven:3.9-eclipse-temurin-17

# Create an unprivileged system user and group for security:
#   groupadd -r app   : -r creates a system group (low GID, no password aging)
#   useradd -rm -g app: -r creates a system user (low UID)
#                       -m forces creation of home directory (/home/app)
#                       -g app sets primary group to 'app'
RUN groupadd -r app && useradd -rm -g app app

# Set execution workspace inside the container
WORKDIR /app
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
ENTRYPOINT ["java", "-jar", "target/calculator.jar"]</code></pre>

            <p>Run these commands in terminal:</p>
            <pre><code class="language-bash"># Build image app1 from Dockerfile in current directory:
#   -t app1  : Tag/name the target image as 'app1'
#   .        : Build context (sends current directory files to Docker daemon)
docker build -t app1 .

# Check image size (approx. 534 MB due to Maven compiler + JDK tools):
docker images app1

# Run container1 non-interactively and verify calculation:
#   -i             : Interactive mode (keeps STDIN open so piped test numbers reach the app)
#   --name container1 : Assigns a human-readable name instead of a random UUID
#   echo "10 3"    : Feeds two numbers into the calculator program
echo "10 3" | docker run -i --name container1 app1

# Clean up container and image:
#   docker rm   : Removes stopped container metadata and write layer
#   docker rmi  : Deletes image from local Docker host cache
docker rm container1 && docker rmi app1</code></pre>

            <h5>Part 2: Build Locally, Package Lean JRE (<code>app2</code>)</h5>
            <p>Build the JAR on your host first (<code>mvn package</code> in Lab 1), then copy <code>target/calculator.jar</code> into <code>part2/</code>.</p>
            <div class="file-links-bar">
                <a href="Docker/Lab3/part2/Dockerfile" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab3/part2/Dockerfile</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-dockerfile"># Base image: Lightweight Java Runtime Environment (JRE 17) only — avoids heavy JDK/compiler tools
FROM eclipse-temurin:17-jre

# Create dedicated non-root application user for least-privilege security:
#   -r       : Creates system group/user (low UID/GID)
#   -m       : Creates home directory (/home/app)
#   -g app   : Assigns primary group 'app'
RUN groupadd -r app && useradd -rm -g app app
WORKDIR /app

# Copy ONLY the pre-compiled JAR artifact from the host build:
#   --chown=app:app : Sets ownership directly on copy to avoid extra intermediate filesystem layers
COPY --chown=app:app calculator.jar .

USER app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "calculator.jar"]</code></pre>

            <pre><code class="language-bash"># Build image app2 from local JAR Dockerfile:
#   -t app2  : Tag/name the target image as 'app2'
#   .        : Current directory build context
docker build -t app2 .

# Check image size (approx. 296 MB — 45% smaller than app1):
docker images app2

# Run container2 and verify with input numbers:
#   -i             : Keeps STDIN open for piped standard input
#   --name container2 : Container instance name
echo "10 3" | docker run -i --name container2 app2

# Clean up container and image:
docker rm container2 && docker rmi app2</code></pre>

            <h5>Bonus: Why the Size Difference Matters</h5>
            <div class="table-container">
                <table>
                    <thead>
                        <tr><th>Image</th><th>Base Image</th><th>Size</th><th>Why It Matters</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><code>app1</code></td><td><code>maven:3.9-eclipse-temurin-17</code></td><td>534 MB</td><td>Holds the compiler, Maven, source code, and cached downloads. Slower to pull and push over the internet.</td></tr>
                        <tr><td><code>app2</code></td><td><code>eclipse-temurin:17-jre</code></td><td>296 MB</td><td>Holds only the Java runtime and the 3.7 KB JAR. Faster to deploy and smaller attack surface.</td></tr>
                    </tbody>
                </table>
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>The Multi-Stage Teaser:</strong> Is there a way to get the best of both worlds (build with zero host tools like Part 1, but get a small 200MB image like Part 2)? Yes! It is called a <strong>Multi-stage build</strong>, which we will do in Lab 4.</li>
                <li><strong>Always use <code>--chown</code> when copying:</strong> If you write <code>COPY . .</code> and then do <code>RUN chown -R app:app /app</code>, Docker creates an extra hidden layer holding another copy of all files, doubling the image size! Writing <code>COPY --chown=app:app . .</code> sets permissions in one single layer.</li>
            </ul>
        """
    },
    {
        "id": "lab-4",
        "number": "Lab 04",
        "title": "Docker Image Optimization and Export/Load",
        "module": "Docker",
        "icon": "⚡",
        "tags": ["Multi-Stage Build", "Alpine Linux", "docker save", "docker load"],
        "summary": "Cut container image size in half using multi-stage builds and Alpine Linux, and learn how to move images between servers without a registry.",
        "question": [
            "Clone the application code from https://github.com/Ibrahim-Adel15/ImageOptimization-.git.",
            "Build an image from the existing Dockerfile with name image1.",
            "Note the image size and run a container named container1 from image1.",
            "Verify that the application is working, then stop and delete the container.",
            "Write a multi-stage Dockerfile and configure the application to run as a non-root user.",
            "Build the optimized image as image2 and compare its size with image1.",
            "Run a container named container2 from image2 and verify that the application is working and running as a non-root user.",
            "Stop and delete container2.",
            "Save image2 as a TAR file named lab-image.tar.",
            "Delete image2 from the local Docker host.",
            "Load the image from image2.tar and verify that it has been restored.",
            "Verify the loaded image is existing in the local Docker host."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>In Lab 3 we saw that building inside Docker made a big 534 MB image, while building locally made a 296 MB image. But what if your production server or CI pipeline doesn't have Maven installed?</p>
            <p><strong>Multi-Stage Builds solve this problem completely:</strong></p>
            <ul>
                <li><strong>Two Rooms in One House:</strong> In your Dockerfile, you can have two <code>FROM</code> lines.
                    <br>&bull; <em>Stage 1 (The Kitchen):</em> Takes the heavy Maven image, compiles your code, and creates the JAR.
                    <br>&bull; <em>Stage 2 (The Dining Table):</em> Starts with a super clean, tiny Alpine Linux JRE image. You reach into Stage 1, grab <em>only</em> the compiled JAR file, and throw away Stage 1 completely!</li>
                <li><strong>What is Alpine Linux?</strong> Normal Linux distributions like Ubuntu or Debian weigh 100+ MB before you even add an app. Alpine Linux is a stripped-down Linux that weighs only 5 MB.</li>
                <li><strong>Saving Images as Files (<code>docker save / load</code>):</strong> How do you move a Docker image to a secure server that has no internet access? You can't use Docker Hub. Instead, <code>docker save</code> packs the image into a <code>.tar</code> zip archive. You copy the file with a USB stick or SCP, and run <code>docker load</code> on the other machine.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Stage 1 (Builder)</span>
                    <span class="node-title">maven:alpine</span>
                    <span class="node-sub">Compiles code & makes JAR</span>
                </div>
                <div class="flow-arrow">➔ Copy JAR Only ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Stage 2 (Runner)</span>
                    <span class="node-title">eclipse-temurin:jre</span>
                    <span class="node-sub">Non-root user (app)</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node success">
                    <span class="node-step">Optimized</span>
                    <span class="node-title">image2 (210 MB)</span>
                    <span class="node-sub">50% Smaller!</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Baseline: Single-Stage Build (<code>image1</code>)</h5>
            <div class="file-links-bar">
                <a href="Docker/Lab4/ImageOptimization/Dockerfile" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab4/ImageOptimization/Dockerfile</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>
            <pre><code class="language-bash"># Clone repository and enter project directory:
git clone https://github.com/Ibrahim-Adel15/ImageOptimization-.git
cd ImageOptimization-

# Build the unoptimized single-stage baseline image:
#   -t image1 : Tag/name the target image as 'image1'
#   .         : Build context (current directory)
docker build -t image1 .
# Size check: 420 MB (carries build tools and intermediate cache)

# Run container1 in detached mode to verify Spring Boot HTTP endpoint:
#   -d             : Detached mode (runs container in background, outputs container ID)
#   --name container1 : Human-readable name instead of randomly generated string
#   -p 8080:8080   : Port forwarding (maps host port 8080 -> container internal port 8080)
docker run -d --name container1 -p 8080:8080 image1

# Send HTTP GET request to verify application is responding:
curl http://localhost:8080/
# Output: Hello from Dockerized Spring Boot!

# Stop and delete container to release port 8080:
#   docker stop : Sends SIGTERM (graceful shutdown) followed by SIGKILL
#   docker rm   : Removes container metadata and writable filesystem layer
docker stop container1 && docker rm container1</code></pre>

            <h5>2. The Multi-Stage Optimized Dockerfile (<code>image2</code>)</h5>
            <div class="file-links-bar">
                <a href="Docker/Lab4/ImageOptimization/Dockerfile.optimized" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab4/ImageOptimization/Dockerfile.optimized</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-dockerfile"># STAGE 1: Builder environment — named 'build' so subsequent stages can reference artifacts
#   AS build : Assigns an alias to this initial build stage
FROM maven:3.9.15-eclipse-temurin-17-alpine AS build
WORKDIR /app
COPY . .
#   -B : Batch mode (non-interactive, suppresses transfer progress output)
RUN mvn package -B

# STAGE 2: Clean, minimal production runtime
FROM eclipse-temurin:17-jre-alpine

# In Alpine (musl libc / busybox), create system group and user:
#   -S     : Create a system group / system user (low UID/GID < 1000)
#   -G app : Assign primary group 'app' to the user
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app

# Copy ONLY the compiled JAR from Stage 1 into Stage 2:
#   --from=build    : Reach into the 'build' stage container filesystem
#   --chown=app:app : Set ownership directly to non-root user during copy
COPY --from=build --chown=app:app /app/target/demo-0.0.1-SNAPSHOT.jar app.jar

USER app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]</code></pre>

            <pre><code class="language-bash"># Build the optimized multi-stage image using the custom Dockerfile:
#   -t image2              : Target image name
#   -f Dockerfile.optimized: Use custom Dockerfile path instead of default ./Dockerfile
#   .                      : Build context
docker build -t image2 -f Dockerfile.optimized .
# Size check: 210 MB (Down from 420 MB - exactly 50% cut!)

# Run container2 and verify:
#   -d           : Detached background execution
#   --name container2 : Container instance name
#   -p 8080:8080 : Map host port 8080 to container port 8080
docker run -d --name container2 -p 8080:8080 image2
curl http://localhost:8080/

# Verify that the container runs as unprivileged user 'app', NOT root:
#   docker exec  : Runs a new process inside an already running container
#   whoami       : Prints effective username inside the container
docker exec container2 whoami
# Output: app

# Clean up container:
docker stop container2 && docker rm container2</code></pre>

            <h5>3. Export and Restore Image as TAR Archive</h5>
            <div class="file-links-bar">
                <a href="Docker/Lab4/lab-image.tar" target="_blank" class="file-pill">
                    <span class="pill-icon">📦</span> <strong>Docker/Lab4/lab-image.tar</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>
            <pre><code class="language-bash"># Save image2 into a portable tar archive:
#   -o lab-image.tar : Output file destination path (creates tar archive of all image layers)
docker save image2 -o lab-image.tar
ls -lh lab-image.tar    # Approx. 201 MB

# Delete image2 from Docker host cache to test restoration:
#   docker rmi : Removes image tag and untagged parent layers from host cache
docker rmi image2
docker images image2    # (empty, confirmed gone)

# Load image back from the tar archive:
#   -i lab-image.tar : Input archive file path to unpack and register into Docker engine
docker load -i lab-image.tar
# Output: Loaded image: image2:latest

# Verify image is back and intact:
docker images image2</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Alpine User Command Difference:</strong> On Ubuntu/Debian you type <code>useradd</code>. On Alpine Linux you must type <code>adduser -S -G app app</code>. If you type <code>useradd</code> on Alpine, Docker throws <code>command not found</code>.</li>
                <li><strong>Image Tarballs for Air-Gapped Environments:</strong> Banks and secure environments often have servers with zero internet access. <code>docker save</code> and <code>docker load</code> are standard tools for delivering software there.</li>
            </ul>
        """
    },
    {
        "id": "lab-5",
        "number": "Lab 05",
        "title": "Docker Image Vulnerability Scanning with Trivy",
        "module": "Docker",
        "icon": "🛡️",
        "tags": ["Trivy", "DevSecOps", "Security Audit", "CVE Remediation"],
        "summary": "Scan Docker images for security holes using Trivy, generate an HTML report, and fix all Critical and High vulnerabilities.",
        "question": [
            "Clone the application and Dockerfile from https://github.com/Ibrahim-Adel15/TrivyImage.git",
            "Build a Docker image from the provided Dockerfile and tag it as trivy-lab:v1.",
            "Install Trivy and verify the installation.",
            "Scan the Docker image for vulnerabilities and review the scan results.",
            "Scan the image to identify only HIGH and CRITICAL vulnerabilities.",
            "Generate an HTML vulnerability report and review the identified security issues.",
            "Bonus: Vulnerability Remediation",
            "  • Investigate the detected HIGH and CRITICAL vulnerabilities.",
            "  • Fix the identified issues by updating the vulnerable base image and application dependencies, where applicable.",
            "  • Rebuild the Docker image and tag it as ivolve-app:v2.",
            "  • Rescan the updated image and generate a new HTML report to verify the remediation.",
            "  • Ensure that no HIGH or CRITICAL vulnerabilities remain, where fixes are available."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>When you write <code>FROM node:18</code> in your Dockerfile, you aren't just downloading Node.js. You are downloading an entire operating system (like Debian) with hundreds of pre-installed system packages: bash, curl, OpenSSL, git, and python.</p>
            <p>If that base image is a few years old, security researchers have already discovered bugs in those packages. Attackers use these bugs (called <strong>CVEs</strong> — Common Vulnerabilities and Exposures) to hack into your servers.</p>
            <p><strong>How Trivy helps:</strong></p>
            <ul>
                <li><strong>The Scanner:</strong> Trivy inspects every package inside your image and checks it against a giant security database. It rates bugs as LOW, MEDIUM, HIGH, or CRITICAL.</li>
                <li><strong>How to Fix 2,000+ Vulnerabilities:</strong>
                    <ol>
                        <li><strong>Upgrade your base image:</strong> Moving from an old Debian image to a modern <code>node:22-alpine</code> cuts out 95% of security bugs because Alpine has far fewer packages installed.</li>
                        <li><strong>Upgrade outdated packages:</strong> Upgrade packages like Express to the latest patch release.</li>
                        <li><strong>Delete tools you don't need:</strong> Production containers only need to <em>run</em> your code with <code>node app.js</code>. They do not need <code>npm</code> or <code>npx</code> inside them anymore! Deleting npm removes its hidden bundled bugs too.</li>
                    </ol>
                </li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-comparison">
                <div class="comparison-card">
                    <div class="comp-badge danger">v1 (Outdated Base)</div>
                    <div class="comp-flow">
                        <span>node:18-bullseye</span> + <span>express 4.18.2</span>
                    </div>
                    <div class="comp-metric danger">2,269 High & Critical CVEs!</div>
                    <div class="comp-note">Heavy Debian packages full of known security bugs.</div>
                </div>
                <div class="comparison-card">
                    <div class="comp-badge success">v2 (Remediated)</div>
                    <div class="comp-flow">
                        <span>node:22-alpine</span> + <span>express 4.21.2</span> + <span>strip npm</span>
                    </div>
                    <div class="comp-metric success">0 High / 0 Critical CVEs!</div>
                    <div class="comp-note">Clean, lean, passes corporate security audit.</div>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Build the Vulnerable Image (<code>v1</code>)</h5>
            <div class="file-links-bar">
                <a href="Docker/Lab5/TrivyImage/Dockerfile" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab5/TrivyImage/Dockerfile</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>
            <pre><code class="language-bash"># Clone repository and enter project directory:
git clone https://github.com/Ibrahim-Adel15/TrivyImage.git
cd TrivyImage

# Build initial image containing outdated Debian bullseye and old Express:
#   -t trivy-lab:v1 : Name and version tag for baseline vulnerable image
#   .               : Build context
docker build -t trivy-lab:v1 .
# Size: approx. 1 GB</code></pre>

            <h5>2. Scan Image with Trivy</h5>
            <pre><code class="language-bash"># Install Trivy security scanner repository and binary (Debian/Ubuntu):
#   -y                     : Automatic yes to installation prompts
#   wget -qO -             : -q quiet mode, -O - writes downloaded key directly to stdout
#   gpg --dearmor -o       : Converts ASCII armored PGP key to binary keyring format
#   tee                    : Reads from stdin and writes to apt source list file
sudo apt install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo gpg --dearmor -o /etc/apt/keyrings/trivy.gpg
echo "deb [signed-by=/etc/apt/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update && sudo apt install -y trivy

# Scan specifically for High and Critical severity vulnerabilities:
#   --severity HIGH,CRITICAL : Filters out low/medium noise to focus on urgent security exploits
trivy image --severity HIGH,CRITICAL trivy-lab:v1</code></pre>
            <div class="terminal-output">
trivy-lab:v1 (debian 11.7)
==========================
Total: 2269 (HIGH: 2048, CRITICAL: 221)
            </div>

            <p>Generate HTML report for the security audit:</p>
            <pre><code class="language-bash"># Render HTML vulnerability report for stakeholder audit:
#   --format template            : Specifies custom templated output
#   --template "@contrib/html.tpl": Uses Trivy's built-in HTML template renderer
#   -o report-v1.html            : Output file path for generated report
trivy image --format template --template "@contrib/html.tpl" -o report-v1.html trivy-lab:v1</code></pre>
            <div class="file-links-bar">
                <a href="Docker/Lab5/report-v1.html" target="_blank" class="file-pill">
                    <span class="pill-icon">📊</span> <strong>Docker/Lab5/report-v1.html</strong> <span class="pill-open">Open Report ↗</span>
                </a>
            </div>

            <h5>3. The Fix: Remediation in <code>TrivyImage-v2/</code></h5>
            <p>We make three key fixes:</p>
            <ol>
                <li>Switch to <code>node:22-alpine</code>.</li>
                <li>Bump Express to <code>^4.21.2</code> in <code>package.json</code>.</li>
                <li>Delete the <code>npm</code> binary after installation to remove internal bundled package issues.</li>
            </ol>

            <div class="file-links-bar">
                <a href="Docker/Lab5/TrivyImage-v2/Dockerfile" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab5/TrivyImage-v2/Dockerfile</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-dockerfile"># Base image: Minimal Alpine Linux with modern Node.js 22 runtime
FROM node:22-alpine
WORKDIR /app
COPY package.json ./

# Install production dependencies only, clean cache, and strip the npm CLI tool:
#   --omit=dev           : Ignores development dependencies (devDependencies)
#   cache clean --force  : Deletes downloaded package tarballs from npm cache
#   rm -rf ...           : Deletes npm and npx binaries (not needed in production containers)
RUN npm install --omit=dev \
    && npm cache clean --force \
    && rm -rf /usr/local/lib/node_modules /usr/local/bin/npm /usr/local/bin/npx

COPY app.js ./
EXPOSE 3000
CMD ["node", "app.js"]</code></pre>

            <pre><code class="language-bash"># Build remediated image:
#   -t ivolve-app:v2 : Tags the clean image version 2
docker build -t ivolve-app:v2 .
# Size: 172 MB (down from 1 GB!)

# Enforce security gate in CI/CD pipelines:
#   --severity HIGH,CRITICAL : Focus on breaking security risks
#   --exit-code 1            : Forces Trivy to return non-zero exit code if matching CVEs are found
trivy image --severity HIGH,CRITICAL --exit-code 1 ivolve-app:v2</code></pre>
            <div class="terminal-output">
ivolve-app:v2 (alpine 3.20.0)
=============================
Total: 0 (HIGH: 0, CRITICAL: 0)
Clean exit code: 0! All Critical and High vulnerabilities eliminated.
            </div>

            <p>Generate the clean verification report:</p>
            <pre><code class="language-bash"># Generate clean audit report demonstrating 0 High / 0 Critical CVEs:
#   -o report-v2.html : Destination HTML audit file
trivy image --format template --template "@contrib/html.tpl" -o report-v2.html ivolve-app:v2</code></pre>
            <div class="file-links-bar">
                <a href="Docker/Lab5/report-v2.html" target="_blank" class="file-pill">
                    <span class="pill-icon">📊</span> <strong>Docker/Lab5/report-v2.html</strong> <span class="pill-open">Open Clean Report ↗</span>
                </a>
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Why did npm have vulnerabilities?</strong> Even in new Node images, the <code>npm</code> CLI tool itself contains older bundled dependencies. Since a running web container never uses npm at runtime, deleting npm after <code>npm install</code> is a trick that cleans up dozens of warnings.</li>
                <li><strong>Automating in CI:</strong> Add <code>--exit-code 1</code> in your Jenkins pipeline. If a developer accidentally adds an insecure package, the pipeline will stop before pushing the image.</li>
            </ul>
        """
    },
    {
        "id": "lab-6",
        "number": "Lab 06",
        "title": "Docker Environment Variables and Resource Management",
        "module": "Docker",
        "icon": "⚙️",
        "tags": ["Resource Limits", "cgroups", "Environment Variables", "docker stats"],
        "summary": "Configure application settings through environment variables and prevent containers from crashing your server using CPU and RAM limits.",
        "question": [
            "Clone the application code from https://github.com/Ibrahim-Adel15/PythonApp.git.",
            "Create a Dockerfile using the python:3.12-slim base image, install the application dependencies, and configure the application to run on port 5000.",
            "Build ivolve1 Docker image.",
            "Run a container with name container1, map port 5000, and configure the environment variables APP_NAME=iVolveApp1 and APP_ENV=stg.",
            "Limit the container resources to 1 CPU and 256 MB of memory.",
            "Verify that the application is working by accessing http://localhost:5000.",
            "Verify the environment variables configured inside the container.",
            "Monitor the container's CPU and memory usage using docker stats cont1.",
            "Create env.txt file with APP_NAME=iVolveApp2 and APP_ENV=prod.",
            "Run a container with name container2, map port 5000, and load the environment variables from env.txt.",
            "Create a new Docker Image with the following environment variables hardcoded in the Dockerfile: APP_NAME=iVolveApp3 and APP_ENV=dev.",
            "Run a container with name container2, map port 5000, and validate the environment variables from Dockerfile."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Two essential habits every DevOps engineer must learn:</p>
            <ul>
                <li><strong>1. Never Hardcode Settings in Code:</strong> Your app needs to run in <code>dev</code> (development on your laptop), <code>stg</code> (staging for testing), and <code>prod</code> (production for real users). If you hardcode the database password or environment name inside the Python file, you have to rewrite the code every time you deploy. Instead, your code reads from <strong>Environment Variables</strong> at startup.</li>
                <li><strong>2. Protect Your Server from Greedy Containers:</strong> By default, a Docker container can take 100% of your computer's CPU and 100% of your RAM. If someone writes a loop with a memory leak, the container will eat all memory and crash your whole operating system!
                    <br>&bull; With <code>--cpus 1</code> and <code>--memory 256m</code>, the Linux kernel puts a fence around the container. It can never use more than its fair share.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Input Options</span>
                    <span class="node-title">-e CLI Flag</span>
                    <span class="node-sub">or --env-file env.txt</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Resource Fence</span>
                    <span class="node-title">cgroups Limits</span>
                    <span class="node-sub">1 CPU + 256 MB RAM</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <span class="node-step">App Reads</span>
                    <span class="node-title">Python Flask</span>
                    <span class="node-sub">Port 5000</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node success">
                    <span class="node-step">Observation</span>
                    <span class="node-title">docker stats</span>
                    <span class="node-sub">Live 24 MB / 256 MB</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Create the Dockerfile</h5>
            <div class="file-links-bar">
                <a href="Docker/Lab6/PythonApp/Dockerfile" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab6/PythonApp/Dockerfile</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-dockerfile"># Base image: Slim Debian Python 3.12 image to reduce footprint
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .

# Install dependencies:
#   --no-cache-dir : Avoids caching wheel/tar downloads, saving ~30 MB in image layer
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]</code></pre>

            <pre><code class="language-bash"># Clone application source code and build Docker image:
#   -t ivolve1 : Assign tag/name 'ivolve1'
#   .          : Build context directory
git clone https://github.com/Ibrahim-Adel15/PythonApp.git
cd PythonApp
docker build -t ivolve1 .</code></pre>

            <h5>2. Run with <code>-e</code> Flags and Resource Limits</h5>
            <p>We publish on port 5001 (in case 5000 is occupied on the host) and set CPU & RAM constraints:</p>
            <pre><code class="language-bash"># Run container1 with runtime environment variables and cgroup limits:
#   -d                 : Run container in background (detached mode)
#   --name container1  : Human-readable container identifier
#   -p 5001:5000       : Port mapping (host port 5001 -> container port 5000)
#   -e APP_NAME=...    : Injects runtime environment variable into process space
#   -e APP_ENV=stg     : Sets environment to 'stg' (staging)
#   --cpus 1           : Limits container to at most 1 CPU core usage
#   --memory 256m      : Sets hard RAM ceiling to 256 Megabytes (triggers OOM kill if exceeded)
docker run -d --name container1 -p 5001:5000 \
  -e APP_NAME=iVolveApp1 -e APP_ENV=stg \
  --cpus 1 --memory 256m ivolve1</code></pre>

            <p>Verify responses, environment variables, and memory caps:</p>
            <pre><code class="language-bash"># Test application HTTP endpoint:
curl http://localhost:5001/
# Returns: {"application":"iVolveApp1","environment":"stg",...}

# Verify environment variables loaded inside running container:
#   docker exec        : Runs command inside running container
#   env | grep APP     : Filters environment variables matching 'APP'
docker exec container1 env | grep APP
# Output:
# APP_NAME=iVolveApp1
# APP_ENV=stg

# Inspect real-time CPU and RAM utilization:
#   --no-stream        : Takes a single snapshot rather than streaming live updates
docker stats --no-stream container1
# Output: container1 | CPU: 0.01% | MEM: 24MiB / 256MiB</code></pre>

            <h5>3. Run with <code>--env-file</code></h5>
            <p>Create an <code>env.txt</code> file:</p>
            <div class="file-links-bar">
                <a href="Docker/Lab6/env.txt" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab6/env.txt</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>
            <pre><code class="language-env">APP_NAME=iVolveApp2
APP_ENV=prod</code></pre>

            <pre><code class="language-bash"># Run container2 reading configuration key-value pairs from an external file:
#   --env-file env.txt : Parses lines in env.txt and exposes them as environment variables
#   -p 5002:5000       : Map to host port 5002
docker run -d --name container2 -p 5002:5000 --env-file env.txt ivolve1

# Verify output reflects production environment:
curl http://localhost:5002/
# Output: {"application":"iVolveApp2","environment":"prod",...}</code></pre>

            <h5>4. Hardcode Defaults in Dockerfile (<code>ENV</code>)</h5>
            <div class="file-links-bar">
                <a href="Docker/Lab6/PythonApp/Dockerfile.env" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab6/PythonApp/Dockerfile.env</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>
            <pre><code class="language-dockerfile"># Build upon base ivolve1 image
FROM ivolve1

# Hardcode fallback environment variables in the image metadata:
#   ENV : Sets persistent environment variables visible during build and runtime
ENV APP_NAME=iVolveApp3
ENV APP_ENV=dev

CMD ["python", "app.py"]</code></pre>

            <pre><code class="language-bash"># Build image ivolve3 using custom Dockerfile:
#   -f Dockerfile.env : Path to custom Dockerfile with hardcoded ENV
docker build -t ivolve3 -f Dockerfile.env .

# Run container3 without passing any -e flags:
docker run -d --name container3 -p 5003:5000 ivolve3

# Verify response picks up hardcoded defaults:
curl http://localhost:5003/
# Output: {"application":"iVolveApp3","environment":"dev",...}</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>What happens when memory is exceeded?</strong> If your container exceeds its 256 MB limit, Linux's Out-Of-Memory (OOM) killer terminates the container immediately with <strong>Exit Code 137</strong>. If your container dies randomly, check <code>docker inspect</code> for <code>OOMKilled: true</code>.</li>
                <li><strong>Security Warning:</strong> Never bake passwords or secret API keys into a Dockerfile using <code>ENV</code>. Anyone who pulls the image can read them with <code>docker history</code>. Use <code>-e</code> or orchestrator secrets instead.</li>
            </ul>
        """
    },
    {
        "id": "lab-7",
        "number": "Lab 07",
        "title": "Multi-Network Microservices, Volumes, and Bind Mounts",
        "module": "Docker",
        "icon": "🕸️",
        "tags": ["Docker Networks", "Bridge Driver", "Named Volumes", "Bind Mounts"],
        "summary": "Connect three microservices using two isolated Docker networks, named volumes for logs, and a host bind mount for persistent messages.",
        "question": [
            "Clone the application code from https://github.com/Ibrahim-Adel15/MicroserviceApp.git.",
            "Create Dockerfiles for the frontend, backend, and notification services, then build their images.",
            "Create two bridge networks with separate subnets: frontend-backend and backend-notification.",
            "Create two docker volumes for backend and notification logs.",
            "Create host directory to persist backend application data and configure a bind mount to map it to the appropriate path inside the backend container.",
            "Run the notification container on backend-notification.",
            "Run the backend container on both networks, configure the notification service URL.",
            "Run the frontend container on frontend-backend, publish port 8080, and configure the backend URL.",
            "Access the web page and verify that messages can be created and retrieved."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>If you put all your containers on one single network, any compromised container can talk to every other container. A user visiting your public website could potentially connect directly to your internal database or notification system.</p>
            <p><strong>The Solution: Network Segmentation & Dual-Homing</strong></p>
            <ul>
                <li><strong>Two Separate Networks:</strong>
                    <br>&bull; Network 1 (<code>frontend-backend</code>): Connects frontend to backend.
                    <br>&bull; Network 2 (<code>backend-notification</code>): Connects backend to notification.
                    <br>&bull; The backend joins <strong>both</strong> networks so it acts as a bridge. The frontend has <strong>no network route</strong> to notification at all!</li>
                <li><strong>Volume vs Bind Mount:</strong>
                    <br>&bull; <em>Named Volume:</em> Managed by Docker in a safe internal location. Ideal for logs that you want Docker to manage.
                    <br>&bull; <em>Host Bind Mount:</em> Links an exact folder on your laptop (e.g. <code>./backend-data</code>) into the container. When the container writes <code>messages.json</code>, you can see and edit the file directly on your desktop.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Public</span>
                    <span class="node-title">Frontend</span>
                    <span class="node-sub">Port 8080</span>
                </div>
                <div class="flow-arrow">➔ [Net: 172.30.0.0/24] ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Bridge</span>
                    <span class="node-title">Backend</span>
                    <span class="node-sub">On Both Networks</span>
                </div>
                <div class="flow-arrow">➔ [Net: 172.31.0.0/24] ➔</div>
                <div class="flow-node">
                    <span class="node-step">Internal</span>
                    <span class="node-title">Notification</span>
                    <span class="node-sub">Hidden from Frontend</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Build the Three Images</h5>
            <pre><code class="language-bash"># Clone microservice repository and build all three container images:
#   -t &lt;name&gt; &lt;dir&gt; : Names image and sets context to service subfolder
git clone https://github.com/Ibrahim-Adel15/MicroserviceApp.git
cd MicroserviceApp

docker build -t frontend frontend
docker build -t backend backend
docker build -t notification notification</code></pre>

            <h5>2. Create Isolated Bridge Networks with Subnets</h5>
            <pre><code class="language-bash"># Create private user-defined bridge networks with explicit CIDR IP blocks:
#   --driver bridge : Uses Docker's software bridge driver (enables automatic container name DNS)
#   --subnet        : Allocates a dedicated IP address range for container IP assignments
docker network create --driver bridge --subnet 172.30.0.0/24 frontend-backend
docker network create --driver bridge --subnet 172.31.0.0/24 backend-notification</code></pre>

            <h5>3. Create Volumes and Host Bind Mount Directory</h5>
            <pre><code class="language-bash"># Create named volumes managed by Docker engine for service logs:
#   docker volume create : Creates persistent storage area in /var/lib/docker/volumes/
docker volume create backend-logs
docker volume create notification-logs

# Create host directory for bind mount to inspect persistent message JSON on the host:
#   mkdir -p : Creates directory including parent directories without error if already exists
mkdir -p backend-data</code></pre>
            <div class="file-links-bar">
                <a href="Docker/Lab7/backend-data" target="_blank" class="file-pill">
                    <span class="pill-icon">📁</span> <strong>Docker/Lab7/backend-data/</strong> <span class="pill-open">Open Folder ↗</span>
                </a>
            </div>

            <h5>4. Run Containers and Connect Networks</h5>
            <pre><code class="language-bash"># 1. Notification (isolated on backend-notification network):
#   --network backend-notification : Attaches container to internal notification subnet
#   -v notification-logs:/app/logs : Mounts named volume to store notification logs
docker run -d --name notification --network backend-notification \
  -v notification-logs:/app/logs notification

# 2. Backend (starts on backend-notification, mounts logs volume and data bind mount):
#   -v backend-logs:/app/logs        : Mounts named volume for backend logs
#   -v $(pwd)/backend-data:/app/data : Host bind mount linking local directory into container
#   -e NOTIFICATION_URL=...          : Injects URL of notification service via Docker DNS
docker run -d --name backend --network backend-notification \
  -v backend-logs:/app/logs \
  -v $(pwd)/backend-data:/app/data \
  -e NOTIFICATION_URL=http://notification:5001/notify backend

# 3. Dual-homing: Connect backend container to the frontend network too!
#   docker network connect : Attaches a secondary network interface to an already running container
docker network connect frontend-backend backend

# 4. Frontend (only on frontend-backend network, exposed on 8080):
#   -p 8080:3000 : Exposes frontend to external users on host port 8080
#   -e BACKEND_URL=http://backend:5000 : Directs frontend API calls to backend container DNS
docker run -d --name frontend --network frontend-backend \
  -p 8080:3000 -e BACKEND_URL=http://backend:5000 frontend</code></pre>

            <h5>5. Verify End-to-End Functionality</h5>
            <pre><code class="language-bash"># Access frontend web page via HTTP GET:
curl http://localhost:8080/

# Submit a message through frontend via HTTP POST:
#   -X POST                : Specifies HTTP request method
#   -d "message=..."       : Sends URL-encoded form data payload in request body
curl -X POST -d "message=Hello from Lab 7" http://localhost:8080/send

# Check host bind mount — verify file written by container exists on host filesystem:
cat backend-data/messages.json
# Output: ["Hello from Lab 7"]

# Check logs in volumes to verify network IP segregation:
#   tail -1 : Displays the last line of the service log
docker exec backend tail -1 /app/logs/backend.log
# Shows requests coming from 172.30.0.x (frontend subnet)

docker exec notification tail -1 /app/logs/notification.log
# Shows requests coming from 172.31.0.x (backend subnet)</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Automatic DNS:</strong> In custom Docker networks, containers can ping each other using their container names (e.g. <code>backend:5000</code>). Docker's embedded DNS server handles this automatically!</li>
                <li><strong>Clean Up:</strong> When finished, remove containers, networks, and volumes in one clean command:
                    <br><code>docker rm -f frontend backend notification && docker network rm frontend-backend backend-notification && docker volume rm backend-logs notification-logs</code></li>
            </ul>
        """
    },
    {
        "id": "lab-8",
        "number": "Lab 08",
        "title": "Containerized Node.js and MySQL Stack Using Docker Compose",
        "module": "Docker",
        "icon": "🐙",
        "tags": ["Docker Compose", "MySQL 8.0", "Node.js", "Docker Hub Push"],
        "summary": "Run a multi-container web application and MySQL database with one single command using Docker Compose, and publish the image to Docker Hub.",
        "question": [
            "Clone the application requirement from https://github.com/Ibrahim-Adel15/iVolveApp.git.",
            "The application requires a MySQL connection and a database named ivolve to start successfully.",
            "Create docker-compose.yml with:",
            "  o App: Build from Dockerfile, map port 3000, configure database environment variables, and persist logs.",
            "  o Database: Use MySQL, configure required environment variables, and persist data using db_data.",
            "  o Network: Create a custom network named ivolve-net for service communication.",
            "  o Volumes: Persist application logs at /app/logs/ and database data at /var/lib/mysql.",
            "Start the services and verify application functionality and connectivity to the DB.",
            "Build and tag the application image with your Docker Hub username, then push it to your repository."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Typing four separate <code>docker run</code> commands with long network and volume flags every time you start your app is tedious and easy to mess up. In real teams, we use <strong>Docker Compose</strong>.</p>
            <ul>
                <li><strong>One Blueprint File (<code>docker-compose.yml</code>):</strong> You describe your entire architecture in one YAML file: what services to run (Node.js app + MySQL database), what ports to open, what database password to use, and where to store data.</li>
                <li><strong>One Command to Start:</strong> You run <code>docker compose up -d</code>. Docker downloads the database, builds your app, creates the private network, attaches the storage volumes, and starts everything in the correct order.</li>
                <li><strong>Publishing to Docker Hub:</strong> Once your app works, you tag the image with your Docker Hub username (<code>docker tag ...</code>) and push it to the cloud (<code>docker push ...</code>). This allows your Kubernetes cluster in the next labs to pull and run your image!</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Stack File</span>
                    <span class="node-title">docker-compose.yml</span>
                    <span class="node-sub">App + MySQL</span>
                </div>
                <div class="flow-arrow">➔ docker compose up ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Network: ivolve-net</span>
                    <span class="node-title">App (3000) ⇄ DB (3306)</span>
                    <span class="node-sub">Volumes: logs + db_data</span>
                </div>
                <div class="flow-arrow">➔ docker push ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Registry</span>
                    <span class="node-title">Docker Hub</span>
                    <span class="node-sub">abdalrahmanx/ivolve-app:v1</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Inspect the Complete <code>docker-compose.yml</code></h5>
            <div class="file-links-bar">
                <a href="Docker/Lab8/iVolveApp/docker-compose.yml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Docker/Lab8/iVolveApp/docker-compose.yml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-yaml">services:
  app:
    build: .                # Builds Dockerfile from current directory
    ports:
      - "3000:3000"         # Host port 3000 -> Container port 3000
    environment:
      DB_HOST: db           # Resolves to MySQL container via Docker internal DNS
      DB_USER: ivolve
      DB_PASSWORD: ivolve123
      DB_NAME: ivolve
    volumes:
      - app_logs:/app/logs  # Named volume storing Node.js application logs
    depends_on:
      - db                  # Ensures db container starts before app
    networks:
      - ivolve-net          # Shared bridge network for service-to-service communication

  db:
    image: mysql:8.0        # Official MySQL 8.0 server image
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: ivolve # Automatically initializes schema on first boot
      MYSQL_USER: ivolve
      MYSQL_PASSWORD: ivolve123
    volumes:
      - db_data:/var/lib/mysql # Persistent storage for MySQL table files
    networks:
      - ivolve-net

networks:
  ivolve-net:
    name: ivolve-net

volumes:
  app_logs:
  db_data:</code></pre>

            <h5>2. Launch Stack and Verify</h5>
            <pre><code class="language-bash"># Launch multi-container stack in background:
#   -d      : Detached mode (runs containers in background)
#   --build : Rebuilds container images before starting, even if local image exists
docker compose up -d --build

# Verify web application health endpoint:
curl http://localhost:3000/health
# Output: iVolve web app is working! Keep calm and code on! [HTTP 200]

# Query MySQL inside database container to confirm initialization:
#   exec db : Executes command inside running 'db' service container
#   -uivolve: Authenticates as MySQL user 'ivolve'
#   -p...   : MySQL user password
#   -e      : Execute SQL query string non-interactively
docker compose exec db sh -c "mysql -uivolve -pivolve123 -e 'SHOW DATABASES;'"
# Lists database: ivolve</code></pre>

            <h5>3. Tag and Push Image to Docker Hub</h5>
            <pre><code class="language-bash"># Authenticate Docker CLI client with your Docker Hub account:
#   -u : Docker Hub username
docker login -u abdalrahmanx

# Tag the built local image with your repository namespace and version:
#   docker tag &lt;source_image&gt; &lt;target_image&gt; : Creates an alias pointing to the same image ID
docker tag ivolveapp-app abdalrahmanx/ivolve-app:v1

# Upload all layers to Docker Hub public registry:
#   docker push : Sends image manifests and blobs to remote registry
docker push abdalrahmanx/ivolve-app:v1</code></pre>
            <div class="terminal-output">
v1: digest: sha256:23d090e3d72bfb467300dc59845170626c47cae6a0cceed645150b18f714a680
Successfully pushed to docker.io/abdalrahmanx/ivolve-app:v1
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Database Cold Start:</strong> Sometimes MySQL takes 5–10 seconds to create its tables on its first boot. If your app crashes immediately on startup, add a health check on the <code>db</code> service so Compose waits until MySQL is truly ready.</li>
                <li><strong>Shutting Down:</strong> Run <code>docker compose down</code> to stop containers without losing database data. If you want to wipe the database and start fresh, run <code>docker compose down -v</code> (the <code>-v</code> flag deletes volumes).</li>
            </ul>
        """
    }
]
