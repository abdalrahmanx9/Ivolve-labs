def call() {
    // -B: Batch mode (disables download progress animation to keep Jenkins console logs clean)
    // test: Runs unit tests
    sh 'mvn -B test'
    // package: Compiles code and packages executable application JAR
    sh 'mvn -B package'
}
