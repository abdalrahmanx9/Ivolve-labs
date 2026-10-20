# Lab 2 — Build & Package the Calculator with Gradle

## 1. Install Gradle

```bash
sudo apt install -y gradle   # Ubuntu
```

```
$ gradle --version
Gradle 8.10.2
```

(JDK 17 required — `build.gradle` pins a 17 toolchain.)

## 2. Clone

```bash
git clone https://github.com/Ibrahim-Adel15/CalculatorGradleApp.git
cd CalculatorGradleApp
```

## 3. Test

```bash
gradle test
```

```
> Task :test
BUILD SUCCESSFUL
```

5/5 pass — see `build/test-results/test/` or open `build/reports/tests/test/index.html`.

## 4. Build

```bash
gradle build
```

```
> Task :jar
BUILD SUCCESSFUL
```

Artifact: `build/libs/calculator.jar` (2.2 KB)

## 5. Run & verify

```bash
java -jar build/libs/calculator.jar
```

```
Enter first number: 10
Enter second number: 3
a = 10.0, b = 3.0
Sum: 13.0
Subtract: 7.0
Multiply: 30.0
Divide: 3.3333333333333335
```

## Maven vs Gradle

| | Maven | Gradle |
|---|---|---|
| Test | `mvn test` | `gradle test` |
| Build | `mvn package` | `gradle build` |
| Artifact | `target/calculator.jar` | `build/libs/calculator.jar` |
| Rebuild | full | incremental |
| Test report | console | HTML in `build/reports/` |
