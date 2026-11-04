def call(String image) {
    sh "sed -i 's|image: abdalrahmanx/ivolve-demoapp:.*|image: ${image}|' Jenkins/Lab21/k8s.yaml"
    sh "grep image: Jenkins/Lab21/k8s.yaml"
    withCredentials([usernamePassword(credentialsId: 'github-push',
            usernameVariable: 'USR', passwordVariable: 'PSW')]) {
        sh 'git config user.email "jenkins@ivolve.local"'
        sh 'git config user.name "jenkins"'
        sh "git add Jenkins/Lab21/k8s.yaml"
        sh "git commit -m 'ci: deploy demoapp ${image}' || echo 'nothing to commit'"
        sh 'git push https://$USR:$PSW@github.com/abdalrahmanx9/Ivolve-labs.git HEAD:main'
    }
}
