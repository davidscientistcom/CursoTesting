import jenkins.model.*
import hudson.security.*
import jenkins.install.*

// Crear usuario admin
def instance = Jenkins.getInstance()
def adminPassword = System.getenv("JENKINS_ADMIN_PASSWORD") ?: "jenkinsadmin2026"
def studentPassword = System.getenv("JENKINS_STUDENT_PASSWORD") ?: "alumno2026"
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount("admin", adminPassword)
hudsonRealm.createAccount("alumno", studentPassword)
instance.setSecurityRealm(hudsonRealm)

// Permisos: admin tiene todo, alumno solo lectura
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)

// Marcar setup como completo
instance.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)
instance.save()

println "=== Jenkins configurado: admin/${adminPassword} + alumno/${studentPassword} ==="
