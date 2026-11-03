import jenkins.model.*
import org.jenkinsci.plugins.workflow.libs.*

def name = 'ivolve-lib'
def existing = GlobalLibraries.get().getLibraries().find { it.name == name }
if (existing == null) {
    def source = new jenkins.plugins.git.GitSCMSource('https://github.com/abdalrahmanx9/ivolve-jenkins-lib.git')
    def lib = new LibraryConfiguration(name, new SCMSourceRetriever(source))
    lib.setDefaultVersion('main')
    lib.setImplicit(false)
    GlobalLibraries.get().getLibraries().add(lib)
    println 'library.groovy: global pipeline library ivolve-lib configured'
}
