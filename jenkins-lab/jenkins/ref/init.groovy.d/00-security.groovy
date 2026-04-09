import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import hudson.security.HudsonPrivateSecurityRealm
import jenkins.install.InstallState
import jenkins.model.Jenkins

def instance = Jenkins.getInstance()
def adminPassword = System.getenv("JENKINS_ADMIN_PASSWORD") ?: "jenkinsadmin2026"
def studentPassword = System.getenv("JENKINS_STUDENT_PASSWORD") ?: "alumno2026"

def hudsonRealm = new HudsonPrivateSecurityRealm(false)
if (hudsonRealm.getUser("admin") == null) {
    hudsonRealm.createAccount("admin", adminPassword)
}
if (hudsonRealm.getUser("alumno") == null) {
    hudsonRealm.createAccount("alumno", studentPassword)
}

instance.setSecurityRealm(hudsonRealm)

def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)
instance.setCrumbIssuer(null)

instance.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)
instance.save()

println "=== Jenkins configurado: admin/${adminPassword} + alumno/${studentPassword} ==="