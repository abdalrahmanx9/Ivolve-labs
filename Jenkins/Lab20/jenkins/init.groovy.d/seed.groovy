import jenkins.model.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import hudson.plugins.git.GitSCM

def instance = Jenkins.get()

if (instance.getItem('demoapp') == null) {
    def job = instance.createProject(WorkflowJob, 'demoapp')
    def scm = new GitSCM('https://github.com/abdalrahmanx9/Ivolve-labs.git')
    job.setDefinition(new CpsScmFlowDefinition(scm, 'Jenkins/Lab21/Jenkinsfile'))
    job.save()
    println 'seed.groovy: demoapp pipeline job created'
}
