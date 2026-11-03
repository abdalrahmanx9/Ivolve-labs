import com.cloudbees.plugins.credentials.CredentialsScope
import com.cloudbees.plugins.credentials.SystemCredentialsProvider
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl
import org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl
import java.nio.file.Files
import java.nio.file.Paths

def env = System.getenv()

def store = SystemCredentialsProvider.getInstance().getStore()

// dockerhub username/password from runtime env (passed to the container, never baked into the image)
if (env.DOCKERHUB_USER && env.DOCKERHUB_TOKEN) {
    def existing = SystemCredentialsProvider.getInstance().credentials.find { it.id == 'dockerhub' }
    if (existing == null) {
        store.addCredentials(
            com.cloudbees.plugins.credentials.domains.Domain.global(),
            new UsernamePasswordCredentialsImpl(
                CredentialsScope.GLOBAL, 'dockerhub', 'Docker Hub push credentials',
                env.DOCKERHUB_USER, env.DOCKERHUB_TOKEN
            )
        )
        println 'credentials.groovy: dockerhub credential added'
    }
}

// kubeconfig mounted from the host (kind cluster, jenkins-sa service account)
def kcPath = env.KUBECONFIG_HOST_PATH ?: '/var/jenkins_extra/kubeconfig'
if (Files.exists(Paths.get(kcPath))) {
    def existingKc = SystemCredentialsProvider.getInstance().credentials.find { it.id == 'kubeconfig' }
    if (existingKc == null) {
        store.addCredentials(
            com.cloudbees.plugins.credentials.domains.Domain.global(),
            new FileCredentialsImpl(
                CredentialsScope.GLOBAL, 'kubeconfig', 'cluster kubeconfig (jenkins-sa)',
                'kubeconfig', com.cloudbees.plugins.credentials.SecretBytes.fromBytes(Files.readAllBytes(Paths.get(kcPath)))
            )
        )
        println 'credentials.groovy: kubeconfig credential added'
    }
}