# generator/module1_buildtools.py

LABS_MODULE_1 = [
    {
        "id": "lab-1",
        "number": "Lab 01",
        "title": "Building and Packaging Java Application with Maven",
        "module": "Build Tools",
        "icon": "☕",
        "tags": ["Java 17", "Apache Maven", "JUnit 5", "JAR Packaging"],
        "summary": "Compile Java source code, run automated tests, and produce a standalone runnable JAR file using Maven.",
        "question": [
            "Install java and maven.",
            "Clone source code https://github.com/Ibrahim-Adel15/CalculatorMavenApp.git",
            "Run unit test.",
            "Build app [ generate artifact in target/calculator.jar ].",
            "Run app.",
            "Verify app is working."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>If you've ever compiled a Java file by typing <code>javac Main.java</code> in your terminal, you know it works for one file. But what happens in a real company where your project has 50 files and needs 15 outside libraries (like database drivers, JSON parsers, or testing tools)?</p>
            <p>Without a build tool, you would have to search the internet, download 15 <code>.jar</code> files by hand, put them into a folder, and type a 200-character terminal command just to compile. If one library needs another library, you get stuck in what developers call <em>"dependency hell"</em>.</p>
            <p><strong>This is where Maven comes in:</strong></p>
            <ul>
                <li><strong>One Shopping List (<code>pom.xml</code>):</strong> You write down the name and version of the libraries you need. Maven goes to the central internet warehouse (Maven Central) and downloads them for you automatically.</li>
                <li><strong>Fixed Standard Folders:</strong> In every Maven project in the world, source code is in <code>src/main/java</code>, tests are in <code>src/test/java</code>, and build outputs go into <code>target/</code>. You never have to guess where files are.</li>
                <li><strong>The Build Lifecycle (Step-by-Step):</strong> Maven runs in predictable phases: it compiles your code, runs your tests with JUnit, and packages everything into an executable <code>.jar</code> file. If a test fails, Maven stops immediately so you never accidentally ship broken code.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Input</span>
                    <span class="node-title">pom.xml + Code</span>
                    <span class="node-sub">src/main/java</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <span class="node-step">Phase 1</span>
                    <span class="node-title">mvn compile</span>
                    <span class="node-sub">Java 17 Bytecode</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <span class="node-step">Phase 2</span>
                    <span class="node-title">mvn test</span>
                    <span class="node-sub">5/5 JUnit Tests Pass</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node success">
                    <span class="node-step">Output</span>
                    <span class="node-title">calculator.jar</span>
                    <span class="node-sub">target/ (3.7 KB)</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Install Java and Maven</h5>
            <p>We need Java 17 (the language runtime) and Maven (the build tool):</p>
            <pre><code class="language-bash"># Update package index and install OpenJDK 17 + Maven build tool:
#   sudo           : Elevate to superuser permissions
#   apt update     : Refresh local package index lists from remote mirrors
#   apt install    : Download and install specified software packages
#   -y             : Automatic 'yes' to prompts (runs non-interactively without pausing)
sudo apt update && sudo apt install -y openjdk-17-jdk maven

# Verify installed runtimes and version information
java -version
mvn -version</code></pre>

            <h5>2. Clone the Application Code</h5>
            <pre><code class="language-bash"># Clone source repository from remote GitHub URL:
#   git clone &lt;url&gt; : Downloads full Git history and working tree
#   cd &lt;directory&gt;  : Change working directory into the project root
git clone https://github.com/Ibrahim-Adel15/CalculatorMavenApp.git
cd CalculatorMavenApp</code></pre>

            <div class="file-links-bar">
                <a href="Build Tools/Lab1/CalculatorMavenApp/pom.xml" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Build Tools/Lab1/CalculatorMavenApp/pom.xml</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <h5>3. Run the Unit Tests</h5>
            <p>Run the automated tests to make sure the calculator math functions work properly before packaging:</p>
            <pre><code class="language-bash"># Execute unit test phase:
#   mvn test : Compiles src/test/java and runs Surefire test runner on CalculatorTest
mvn test</code></pre>
            <div class="terminal-output">
[INFO] Scanning for projects...
[INFO] Running com.calculator.CalculatorTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
            </div>

            <h5>4. Package the App into a JAR</h5>
            <p>Compile the code and generate the final executable <code>.jar</code> file inside the <code>target/</code> folder:</p>
            <pre><code class="language-bash"># Compile, test, and package application into target/calculator.jar:
#   mvn package : Executes default lifecycle phases (validate -> compile -> test -> package)
mvn package</code></pre>
            <div class="terminal-output">
[INFO] --- maven-jar-plugin:3.3.0:jar (default-jar) @ calculator ---
[INFO] Building jar: .../target/calculator.jar
[INFO] BUILD SUCCESS
            </div>

            <h5>5. Run and Verify</h5>
            <p>Run the generated JAR directly using the Java runtime. We pipe numbers so it runs automatically:</p>
            <pre><code class="language-bash"># Pass test input numbers (10 and 3) into the calculator program via standard input:
#   echo "10 3"    : Emits test numbers to standard output
#   |              : Linux pipe redirects stdout of echo into stdin of java process
#   java -jar      : Executes executable JAR archive using Main-Class defined in pom.xml
echo "10 3" | java -jar target/calculator.jar</code></pre>
            <div class="terminal-output">
Enter first number: Enter second number: a = 10.0, b = 3.0
Sum: 13.0
Subtract: 7.0
Multiply: 30.0
Divide: 3.3333333333333335
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Skipping Tests in CI:</strong> You might see people use <code>mvn package -DskipTests</code> to build faster. In production CI/CD pipelines, never skip tests—that's how broken code slips into production.</li>
                <li><strong>Clean Builds:</strong> If you ever change code and the JAR doesn't seem to update, run <code>mvn clean package</code>. The <code>clean</code> command wipes out the old <code>target/</code> folder so everything rebuilds fresh.</li>
            </ul>
        """
    },
    {
        "id": "lab-2",
        "number": "Lab 02",
        "title": "Building and Packaging Application with Gradle",
        "module": "Build Tools",
        "icon": "🐘",
        "tags": ["Gradle 8", "Java/JVM", "Build Cache", "Fast Incremental Builds"],
        "summary": "Build the calculator application using Gradle to understand modern incremental builds, Gradle tasks, and HTML test reports.",
        "question": [
            "Install Gradle.",
            "Clone source code https://github.com/Ibrahim-Adel15/CalculatorGradleApp.git",
            "Run unit test.",
            "Build app [ generate artifact in build/libs/calculator.jar ].",
            "Run app.",
            "Verify app is working."
        ],
        "concept": """
            <h4>The Core Idea & Concepts</h4>
            <p>Maven is great, but its XML files can get very long and messy. Also, Maven rebuilds everything from scratch each time. If your project takes 20 minutes to compile, waiting that long every time you change one line of code slows you down.</p>
            <p><strong>Gradle</strong> was created to solve this:</p>
            <ul>
                <li><strong>No Rigid XML:</strong> Gradle uses readable code (Groovy or Kotlin) in a file called <code>build.gradle</code> instead of XML.</li>
                <li><strong>Smart "Incremental" Builds:</strong> Gradle checks what changed since the last build. If you didn't touch a file, Gradle marks it as <code>UP-TO-DATE</code> and skips it. This makes builds up to 10x faster than Maven.</li>
                <li><strong>The Background Daemon:</strong> Gradle keeps a small worker process running in the background on your computer so it doesn't have to start up the JVM from zero every time you run a command.</li>
                <li><em>Slide note:</em> The slide title mentions Go with Gradle, but the lab uses Gradle to compile the Java calculator. Gradle can build Go, C++, or Android apps, but here we focus on comparing how Gradle builds the same Java app compared to Maven.</li>
            </ul>
        """,
        "diagram_html": """
            <div class="visual-flow">
                <div class="flow-node">
                    <span class="node-step">Config</span>
                    <span class="node-title">build.gradle</span>
                    <span class="node-sub">Task Graph</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <span class="node-step">Task</span>
                    <span class="node-title">gradle test</span>
                    <span class="node-sub">HTML Report in build/</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <span class="node-step">Task</span>
                    <span class="node-title">gradle build</span>
                    <span class="node-sub">Incremental Compile</span>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node success">
                    <span class="node-step">Output</span>
                    <span class="node-title">calculator.jar</span>
                    <span class="node-sub">build/libs/ (2.2 KB)</span>
                </div>
            </div>
        """,
        "solving": """
            <h4>Step-by-Step Solution & Commands</h4>

            <h5>1. Install Gradle</h5>
            <pre><code class="language-bash"># Update package list and install Gradle:
#   -y : Automatically answers yes to installation prompts for non-interactive execution
sudo apt update && sudo apt install -y gradle

# Check Gradle and JVM runtime version
gradle --version</code></pre>

            <h5>2. Clone the Repository</h5>
            <pre><code class="language-bash"># Clone Gradle calculator codebase and navigate into project directory
git clone https://github.com/Ibrahim-Adel15/CalculatorGradleApp.git
cd CalculatorGradleApp</code></pre>

            <div class="file-links-bar">
                <a href="Build Tools/Lab2/CalculatorGradleApp/build.gradle" target="_blank" class="file-pill">
                    <span class="pill-icon">📄</span> <strong>Build Tools/Lab2/CalculatorGradleApp/build.gradle</strong> <span class="pill-open">Open ↗</span>
                </a>
            </div>

            <h5>3. Run Unit Tests & View HTML Report</h5>
            <pre><code class="language-bash"># Run test task:
#   gradle test : Compiles test code and executes JUnit test suite
gradle test</code></pre>
            <div class="terminal-output">
> Task :compileJava UP-TO-DATE
> Task :test
BUILD SUCCESSFUL in 850ms
            </div>
            <p>Unlike Maven which only outputs text to the console, Gradle generates a ready-to-view HTML dashboard at <code>build/reports/tests/test/index.html</code>.</p>

            <h5>4. Build the App</h5>
            <pre><code class="language-bash"># Execute full application build:
#   gradle build : Runs compileJava, processResources, classes, jar, and test tasks
#   Output artifact: build/libs/calculator.jar (approx. 2.2 KB)
gradle build</code></pre>
            <div class="terminal-output">
> Task :jar
> Task :build
BUILD SUCCESSFUL in 1s
            </div>
            <p>Artifact created: <code>build/libs/calculator.jar</code> (approx. 2.2 KB).</p>

            <h5>5. Run and Verify</h5>
            <pre><code class="language-bash"># Verify standalone execution by piping input numbers into Java runtime:
#   echo "10 3"    : Inputs for calculation
#   java -jar      : Executes the packaged standalone JAR from build/libs
echo "10 3" | java -jar build/libs/calculator.jar</code></pre>
            <div class="terminal-output">
Enter first number: Enter second number: a = 10.0, b = 3.0
Sum: 13.0
Subtract: 7.0
Multiply: 30.0
Divide: 3.3333333333333335
            </div>

            <h5>Maven vs Gradle Quick Summary</h5>
            <div class="table-container">
                <table>
                    <thead>
                        <tr><th>Feature</th><th>Maven</th><th>Gradle</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Configuration</td><td><code>pom.xml</code> (XML)</td><td><code>build.gradle</code> (Code)</td></tr>
                        <tr><td>Build Speed</td><td>Rebuilds all steps</td><td>Incremental (skips unchanged files)</td></tr>
                        <tr><td>Output Location</td><td><code>target/calculator.jar</code></td><td><code>build/libs/calculator.jar</code></td></tr>
                    </tbody>
                </table>
            </div>
        """,
        "tips": """
            <h4>Tips</h4>
            <ul>
                <li><strong>Always use <code>./gradlew</code>:</strong> In real projects, you will see a <code>gradlew</code> file. That is the "Gradle Wrapper". It ensures everyone on the team and all automated servers use the exact same version of Gradle without manual installation.</li>
                <li><strong>Where did the JAR go?</strong> Remember: Maven outputs to <code>target/</code>, while Gradle outputs to <code>build/libs/</code>.</li>
            </ul>
        """
    }
]
