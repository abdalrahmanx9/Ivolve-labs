# generator/module4_jenkins.py

LABS_MODULE_4 = [
    {
        "id": "lab-20",
        "number": "Lab 20",
        "title": "Role-Based Authorization in Jenkins",
        "module": "Jenkins CI/CD",
        "icon": "👨‍💼",
        "tags": ["Jenkins", "RBAC", "Matrix Security", "Jenkins as Code"],
        "summary": "Configure Jenkins user permissions automatically at startup using Groovy code so user1 has full admin rights and user2 has read-only access.",
        "question": [
            "Create user1 and user2 in Jenkins.",
            "Assign admin role for user1 & read-only role for user2."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>If you set up Jenkins by clicking buttons in the web UI, what happens when your server hard drive crashes? You have to click all those buttons again by hand.</p>
            <p>In modern DevOps, we practice <strong>Configuration as Code</strong>:</p>
            <ul>
                <li><strong>Automated Setup via Groovy:</strong> Jenkins lets you place <code>.groovy</code> scripts in an <code>init.groovy.d/</code> folder. When Jenkins turns on, it runs these scripts automatically and configures itself without human intervention.</li>
                <li><strong>User 1 (The Administrator):</strong> Has <code>Jenkins.ADMINISTER</code> permissions. They can create jobs, install plugins, edit system settings, and trigger deployments.</li>
                <li><strong>User 2 (The Read-Only Stakeholder):</strong> Has <code>Jenkins.READ</code>, <code>Item.READ</code>, and <code>View.READ</code>. They can log in, view build history, and read console logs. But if they try to click "Build Now" or edit job settings, Jenkins blocks them with a <code>403 Forbidden</code> error!</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-comparison">
                <div class="comparison-card">
                    <div class="comp-badge success">user1 (Administrator)</div>
                    <div class="comp-flow">Jenkins.ADMINISTER ➔ Full Access</div>
                    <div class="comp-metric success">Can Build & Configure</div>
                    <div class="comp-note">POST /job/.../build ➔ HTTP 201 Created</div>
                </div>
                <div class="comparison-card">
                    <div class="comp-badge danger">user2 (Read-Only)</div>
                    <div class="comp-flow">Item.READ only ➔ View Dashboard Only</div>
                    <div class="comp-metric danger">Cannot Trigger Builds</div>
                    <div class="comp-note">POST /job/.../build ➔ HTTP 403 Forbidden</div>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. The Security Initialization Script</h5>
            <p>Inspect the script that configures Jenkins users at boot:</p>
            <div class="file-links-bar">
                <a href="Jenkins/Lab20/jenkins/init.groovy.d/security.groovy" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Jenkins/Lab20/jenkins/init.groovy.d/security.groovy</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-groovy">import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()

// Create the user accounts
def realm = new HudsonPrivateSecurityRealm(false)
realm.createAccount('user1', 'admin123')
realm.createAccount('user2', 'read123')
instance.setSecurityRealm(realm)

// Configure the Matrix Authorization Table
def strategy = new GlobalMatrixAuthorizationStrategy()

// user1 gets full administrator power:
strategy.add(Jenkins.ADMINISTER, 'user1')

// user2 gets read-only permissions:
strategy.add(Jenkins.READ, 'user2')
strategy.add(hudson.model.Item.READ, 'user2')
strategy.add(hudson.model.Item.DISCOVER, 'user2')
strategy.add(hudson.model.View.READ, 'user2')

instance.setAuthorizationStrategy(strategy)
instance.save()
println("--> RBAC Security Configuration Applied Successfully!")</code></pre>

            <h5>2. Run Dockerized Jenkins with Volume Mounts</h5>
            <div class="file-links-bar">
                <a href="Jenkins/Lab20/jenkins/Dockerfile" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Jenkins/Lab20/jenkins/Dockerfile</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-bash"># Build customized Jenkins image:
#   -t jenkins-ivolve : Tags output image with friendly name
docker build -t jenkins-ivolve Jenkins/Lab20/jenkins

# Start Jenkins container exposing port 8888:
#   -d                               : Detached mode (runs container in background)
#   --name jenkins                   : Container instance identifier
#   -p 8888:8080                     : Maps host port 8888 to Jenkins internal web UI port 8080
#   -v jenkins_home:/var/jenkins_home: Named volume preserving job definitions, workspace history, and plugin configs
#   -v /var/run/docker.sock:...      : Mounts host Docker daemon socket so Jenkins can build images without nested virtualization
#   -e DOCKERHUB_USER / TOKEN        : Passes environment variables into container for pipeline automation
docker run -d --name jenkins -p 8888:8080 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DOCKERHUB_USER=abdalrahmanx -e DOCKERHUB_TOKEN=&lt;TOKEN&gt; \
  jenkins-ivolve</code></pre>

            <h5>3. Verify Permissions (UI & REST API)</h5>
            <pre><code class="language-bash"># Test 1: Admin user triggering a build (ALLOWED - 201 Created):
#   -u user1:admin123 : Basic Authentication HTTP header credentials
#   -X POST           : Sends HTTP POST method required by Jenkins build endpoint
curl -u user1:admin123 http://localhost:8888/job/demoapp/build -X POST
# Response: HTTP 201 (Build triggered!)

# Test 2: Read-only user trying to trigger a build (BLOCKED - 403 Forbidden):
#   -u user2:read123  : Authenticates as read-only user lacking Job/Build permission
curl -u user2:read123 http://localhost:8888/job/demoapp/build -X POST
# Response: HTTP 403 Forbidden! User2 lacks build permission.</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>The Overall READ Requirement:</strong> In Jenkins Matrix security, you must always grant <code>Jenkins.READ</code> to a user before anything else. If you grant <code>Item.READ</code> but forget <code>Jenkins.READ</code>, the user won't even be able to open the login dashboard!</li>
            </ul>
        """
    },
    {
        "id": "lab-21",
        "number": "Lab 21",
        "title": "Jenkins Pipeline for Application Deployment",
        "module": "Jenkins CI/CD",
        "icon": "🔄",
        "tags": ["Jenkinsfile", "CI/CD Pipeline", "Trivy Scan", "Rolling Update"],
        "summary": "Build a complete 7-stage automated pipeline in Jenkins that tests code, builds Docker images, scans for security flaws, and updates Kubernetes.",
        "question": [
            "Clone source code and Dockerfile from: https://github.com/Ibrahim-Adel15/DemoApp.git",
            "Create a pipeline that automates the following processes:",
            "  1. Build app",
            "  2. Build Docker Image.",
            "  3. Scan Docker Image",
            "  4. Push image to DockerHub.",
            "  5. Delete image locally.",
            "  6. Update image in deployment file.",
            "  7. Deploy to Kubernetes cluster.",
            "Set pipeline post action (always, success, failure)"
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Every time a developer writes new code, we don't want them doing 10 manual steps on their laptop (compiling, building docker, logging into docker hub, running kubectl). Manual steps lead to human mistakes.</p>
            <p>A <strong>CI/CD Pipeline</strong> is an automated robot script (written in a <code>Jenkinsfile</code>):</p>
            <ul>
                <li><strong>The 7 Automated Steps:</strong>
                    <ol>
                        <li><strong>Compile:</strong> Builds the Spring Boot JAR with Maven.</li>
                        <li><strong>Package:</strong> Builds the Docker image and tags it with the build number (e.g. <code>:1</code>, <code>:2</code>).</li>
                        <li><strong>Security Audit:</strong> Scans the image with Trivy to check for security vulnerabilities.</li>
                        <li><strong>Publish:</strong> Uploads the verified image to Docker Hub.</li>
                        <li><strong>Clean Disk:</strong> Deletes the local image on the build server so the server hard drive never runs out of space.</li>
                        <li><strong>Patch Manifest:</strong> Replaces the old image tag in <code>k8s.yaml</code> with the new build number.</li>
                        <li><strong>Deploy:</strong> Runs <code>kubectl apply</code> using the limited ServiceAccount token from Lab 19 to trigger a rolling update in Kubernetes!</li>
                    </ol>
                </li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">1 & 2</span>
                    <span class="node-title">Maven + Docker</span>
                    <span class="node-sub">Builds JAR & Image</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <span class="node-step">3 & 4</span>
                    <span class="node-title">Trivy + Registry</span>
                    <span class="node-sub">Scans & Pushes to Hub</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">5 & 6</span>
                    <span class="node-title">Clean + Patch</span>
                    <span class="node-sub">sed image tag in YAML</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node success">
                    <span class="node-step">7. Deploy</span>
                    <span class="node-title">kubectl apply</span>
                    <span class="node-sub">Zero-Downtime Rollout</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. The Complete Declarative <code>Jenkinsfile</code></h5>
            <div class="file-links-bar">
                <a href="Jenkins/Lab21/Jenkinsfile" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Jenkins/Lab21/Jenkinsfile</strong> <span class="pill-open">Open ↗</span>
                </a>
                <a href="Jenkins/Lab21/k8s.yaml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Jenkins/Lab21/k8s.yaml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-groovy">pipeline {
    agent any

    environment {
        APP_NAME     = 'ivolve-demoapp'
        REGISTRY     = 'abdalrahmanx'
        IMAGE_NAME   = "${REGISTRY}/${APP_NAME}"
        DOCKER_CREDS = 'dockerhub'
        KUBECONFIG   = credentials('kubeconfig')
    }

    stages {
        stage('1. Build app') {
            steps {
                dir('Jenkins/Lab21/DemoApp') {
                    // -B: Batch mode (disables interactive prompts & progress spinner animation)
                    // clean: Deletes previous target/ build artifacts
                    // package: Compiles code, runs unit tests, packages into JAR
                    sh 'mvn -B clean package'
                }
            }
        }

        stage('2. Build Docker Image') {
            steps {
                dir('Jenkins/Lab21/DemoApp') {
                    // -t &lt;name:tag&gt;: Names and tags the image with the unique Jenkins BUILD_NUMBER
                    // .            : Build context path containing Dockerfile and compiled JAR
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                }
            }
        }

        stage('3. Scan Docker Image') {
            steps {
                // --severity HIGH,CRITICAL: Limits vulnerability report to actionable high-risk flaws
                // --exit-code 0           : Runs security audit in non-blocking advisory mode so pipeline completes
                sh "trivy image --severity HIGH,CRITICAL --exit-code 0 ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('4. Push image to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDS,
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    // --password-stdin: Pipes secret from standard input avoiding shell history leakage
                    // -u &lt;user&gt;       : Docker Hub account username
                    sh "echo \\$PASS | docker login -u \\$USER --password-stdin"
                    sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }

        stage('5. Delete image locally') {
            steps {
                // rmi: Removes local image from Jenkins host to prevent hard drive saturation
                sh "docker rmi ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('6. Update image in deployment file') {
            steps {
                // -i: Edits file in-place
                // s|old|new|g: Regex replaces the image tag in Kubernetes manifest with current build number
                sh "sed -i 's|image: ${IMAGE_NAME}:.*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g' Jenkins/Lab21/k8s.yaml"
            }
        }

        stage('7. Deploy to Kubernetes cluster') {
            steps {
                // --kubeconfig: Passes authenticated ServiceAccount credentials from Lab 19
                // -f          : Specifies target Kubernetes manifest file
                sh "kubectl --kubeconfig \\$KUBECONFIG apply -f Jenkins/Lab21/k8s.yaml"
                // rollout status: Blocks pipeline execution until deployment update reaches Ready state
                sh "kubectl --kubeconfig \\$KUBECONFIG rollout status deployment/demoapp -n ivolve"
            }
        }
    }

    post {
        always {
            echo "Pipeline run completed for build #${BUILD_NUMBER}."
        }
        success {
            echo "Deployment succeeded! Pods are live in the ivolve namespace."
        }
        failure {
            echo "Deployment failed! Check the stage logs above for error details."
        }
    }
}</code></pre>

            <h5>2. Run Build and Verify in Kubernetes</h5>
            <pre><code class="language-bash"># Verify deployment in cluster:
#   -n ivolve      : Scope query to ivolve namespace
#   -l app=demoapp : Filter pods matching selector label
kubectl get pods -n ivolve -l app=demoapp
# Output: demoapp-...  1/1  Running

# Test HTTP output:
#   exec deployment/demoapp : Connects to an active replica pod of the deployment
#   -n ivolve               : Target namespace
#   --                      : Delimiter separating kubectl flags from container command
#   wget -qO-               : -q quiet mode (no progress bar), -O- streams body directly to stdout
kubectl exec deployment/demoapp -n ivolve -- wget -qO- http://demoapp-svc:8080/
# Output: Hello from Dockerized Spring Boot!</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Why Delete the Image Locally in Stage 5?</strong> In an active company, Jenkins builds images 50 times a day. If you don't run <code>docker rmi</code> to delete local copies after pushing to Docker Hub, your build server's hard drive will fill up and crash within a month.</li>
            </ul>
        """
    },
    {
        "id": "lab-22",
        "number": "Lab 22",
        "title": "CI/CD Pipeline Implementation with Jenkins Agents and Shared Libraries",
        "module": "Jenkins CI/CD",
        "icon": "📚",
        "tags": ["Shared Libraries", "Docker Agent", "DRY Principle", "Build Caching"],
        "summary": "Avoid duplicating pipeline code across projects by writing reusable Jenkins Shared Libraries and running build steps inside dynamic Docker agent containers.",
        "question": [
            "Clone Dockerfile from: https://github.com/Ibrahim-Adel15/DemoApp.git",
            "Create the following shared libraries:",
            "  1. BuildApp (Unit test, Build app)",
            "  2. BuildImage (Build image, scan image push image, delete image locally)",
            "  3. DeployOnK8s (edit deployment file, deploy to cluster)",
            "Update your pipeline to use them.",
            "Configure Jenkins slave to run the pipeline."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>If your company has 40 microservices, do you want to copy and paste the same 100-line <code>Jenkinsfile</code> into all 40 repositories? No! If a command changes, you have to edit 40 files.</p>
            <p><strong>Two Techniques for Professional CI/CD:</strong></p>
            <ul>
                <li><strong>1. Jenkins Shared Libraries (Don't Repeat Yourself - DRY):</strong> You write your build functions once in a shared Git repository. Your microservices just import the library with <code>@Library('ivolve-lib') _</code> and call clean one-liners like <code>buildApp()</code> or <code>buildImage()</code>.</li>
                <li><strong>2. Dynamic Docker Agents ("Slaves"):</strong> Instead of running Maven directly on the main Jenkins controller, Jenkins spins up an isolated Docker container (<code>maven:3.9</code>) just for the build step. When the build finishes, the container is destroyed.
                    <br>&bull; A shared volume (<code>ivolve-maven-repo:/root/.m2</code>) caches downloaded dependencies so builds stay fast.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Controller</span>
                    <span class="node-title">Loads Library</span>
                    <span class="node-sub">@Library('ivolve-lib')</span>
                </div>
                <div class="flow-arrow">➔ Spins Up ➔</div>
                <div class="flow-node highlight">
                    <span class="node-step">Ephemeral Agent</span>
                    <span class="node-title">maven:3.9 container</span>
                    <span class="node-sub">Cached .m2 Volume</span>
                </div>
                <div class="flow-arrow">➔ Calls Steps ➔</div>
                <div class="flow-node success">
                    <span class="node-step">Modular Pipeline</span>
                    <span class="node-title">buildApp()</span>
                    <span class="node-sub">buildImage() ➔ deployOnK8s()</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Structure of the Shared Library</h5>
            <p>Inspect the three modular Groovy functions in the library:</p>
            <div class="file-links-bar">
                <a href="Jenkins/Lab22/lib/vars/buildApp.groovy" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>vars/buildApp.groovy</strong> <span class="pill-open">Open ↗</span>
                </a>
                <a href="Jenkins/Lab22/lib/vars/buildImage.groovy" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>vars/buildImage.groovy</strong> <span class="pill-open">Open ↗</span>
                </a>
                <a href="Jenkins/Lab22/lib/vars/deployOnK8s.groovy" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>vars/deployOnK8s.groovy</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <pre><code class="language-groovy">// vars/buildApp.groovy:
def call() {
    // -B: Batch mode (disables download animation to keep Jenkins console clean)
    // clean package: Cleans old artifacts and packages compiled JAR
    sh 'mvn -B clean package'
}

// vars/buildImage.groovy:
def call(String imageTag) {
    // -t &lt;tag&gt;: Tags image with repo/name:build_id
    sh "docker build -t ${imageTag} Jenkins/Lab21/DemoApp"
    // --severity HIGH,CRITICAL: Focuses scan on high-risk CVEs
    // --exit-code 0           : Runs security scan without failing build
    sh "trivy image --severity HIGH,CRITICAL --exit-code 0 ${imageTag}"
    withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                      usernameVariable: 'U',
                                      passwordVariable: 'P')]) {
        // --password-stdin: Safely passes password via stdin
        sh "echo \\$P | docker login -u \\$U --password-stdin"
        sh "docker push ${imageTag}"
    }
    // rmi: Deletes local image copy to reclaim worker disk space
    sh "docker rmi ${imageTag}"
}

// vars/deployOnK8s.groovy:
def call(String imageTag) {
    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
        // -i: In-place edit of Kubernetes manifest with target image
        sh "sed -i 's|image: .*|image: ${imageTag}|g' Jenkins/Lab21/k8s.yaml"
        // --kubeconfig: Authenticates via scoped ServiceAccount token
        // -f          : Path to manifest to apply
        sh "kubectl --kubeconfig \\$KUBECONFIG apply -f Jenkins/Lab21/k8s.yaml"
    }
}</code></pre>

            <h5>2. The Refactored Clean <code>Jenkinsfile</code></h5>
            <pre><code class="language-groovy">@Library('ivolve-lib') _

pipeline {
    agent any

    stages {
        stage('Build app') {
            agent {
                docker {
                    image 'maven:3.9-eclipse-temurin-17'
                    // -v: Mounts persistent named volume caching ~/.m2 repository across agent container lifecycles
                    args '-v ivolve-maven-repo:/root/.m2'  // Cache downloads
                    reuseNode true                        // Stay in the same folder!
                }
            }
            steps {
                dir('Jenkins/Lab21/DemoApp') {
                    buildApp()                            // One clean line!
                }
            }
        }

        stage('Build and push image') {
            steps {
                script {
                    buildImage("abdalrahmanx/ivolve-demoapp:${BUILD_NUMBER}")
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    deployOnK8s("abdalrahmanx/ivolve-demoapp:${BUILD_NUMBER}")
                }
            }
        }
    }
}</code></pre>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>The <code>reuseNode true</code> Gotcha:</strong> When you run a Docker agent inside a stage, Jenkins creates a separate folder (like <code>demoapp@2</code>). If you build your JAR there and switch back to the controller, the controller looks in <code>demoapp</code> and can't find the JAR! Setting <code>reuseNode true</code> forces the Docker agent to share the exact same workspace.</li>
            </ul>
        """
    }
]
