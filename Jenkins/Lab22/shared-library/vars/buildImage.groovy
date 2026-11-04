def call(String image) {
    // -t <name:tag>: Names and tags the image with the repository and build tag
    // Jenkins/Lab21/DemoApp: Path to build context containing the Dockerfile
    sh "docker build -t ${image} Jenkins/Lab21/DemoApp"

    // --exit-code 0           : Runs security scan in advisory mode (does not break pipeline)
    // --severity HIGH,CRITICAL: Filters vulnerability scanner to report only high and critical CVEs
    sh "trivy image --exit-code 0 --severity HIGH,CRITICAL ${image}"

    withCredentials([usernamePassword(credentialsId: 'dockerhub',
            usernameVariable: 'USR', passwordVariable: 'PSW')]) {
        // --password-stdin: Safely passes password from standard input without exposing it in process tables
        // -u <username>   : Docker Hub username
        sh 'echo "$PSW" | docker login -u "$USR" --password-stdin'
        sh "docker push ${image}"
    }

    // rmi: Removes local image from worker disk to prevent storage exhaustion
    sh "docker rmi ${image}"
}
