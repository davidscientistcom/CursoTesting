import hudson.plugins.git.BranchSpec
import hudson.plugins.git.GitSCM
import hudson.plugins.git.UserRemoteConfig
import hudson.triggers.SCMTrigger
import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

hudson.plugins.git.GitStatus.NOTIFY_COMMIT_ACCESS_CONTROL = 'disabled-for-polling'

def jenkins = Jenkins.getInstance()
def repoUrl = 'http://gitea:3000/alumno/jenkins-python-lab.git'
def jobName = 'jenkins-python-lab'

WorkflowJob job = jenkins.getItem(jobName)
if (job == null) {
    job = jenkins.createProject(WorkflowJob, jobName)
}

job.setDescription('Laboratorio CI para Jenkins + Gitea + pytest + MariaDB.')

def scm = new GitSCM(
    [new UserRemoteConfig(repoUrl, null, null, null)],
    [new BranchSpec('*/main')],
    false,
    [],
    null,
    null,
    []
)

def definition = new CpsScmFlowDefinition(scm, 'Jenkinsfile')
definition.setLightweight(true)
job.setDefinition(definition)

def existingTrigger = job.getTriggers().get(SCMTrigger.class)
if (existingTrigger == null) {
    job.addTrigger(new SCMTrigger('H/5 * * * *'))
}

job.save()

println "=== Job ${jobName} preparado para ${repoUrl} ==="