# Lab 1 — Build & Package a Java App with Maven

## 1. Install Java and Maven

```bash
sudo apt install -y openjdk-17-jdk maven   # Ubuntu
```

```
$ java -version
openjdk version "17.0.20.1"

$ mvn -version
Apache Maven 3.9.9
```

## 2. Clone

```bash
git clone https://github.com/Ibrahim-Adel15/CalculatorMavenApp.git
cd CalculatorMavenApp
```

## 3. Test

```bash
mvn test
```

```
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

## 4. Package

```bash
mvn package
```

```
[INFO] Building jar: ...\target\calculator.jar
[INFO] BUILD SUCCESS
```

Artifact: `target/calculator.jar` (3.7 KB)

## 5. Run & verify

```bash
java -jar target/calculator.jar
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

Non-interactive: `echo "10 3" | java -jar target/calculator.jar`
