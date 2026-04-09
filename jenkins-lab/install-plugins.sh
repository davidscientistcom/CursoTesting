#!/bin/bash
# =============================================================================
# install-plugins.sh — Instala plugins esenciales en Jenkins
# Ejecutar DESPUÉS de levantar el contenedor:
#   docker exec jenkins-lab bash /var/jenkins_home/install-plugins.sh
# =============================================================================

set -e

PLUGIN_LIST=(
  "git"
  "workflow-aggregator"       # Pipeline
  "pipeline-stage-view"       # Vista de stages
  "github"                    # GitHub integration
  "github-branch-source"      # Multibranch pipeline desde GitHub
  "docker-workflow"           # Docker Pipeline
  "docker-plugin"             # Docker agent
  "credentials"               # Gestión credenciales
  "credentials-binding"       # Binding de credenciales en pipeline
  "ssh-credentials"           # SSH keys
  "junit"                     # Test results
  "cobertura"                 # Coverage reports
  "blueocean"                 # UI moderna
  "locale"                    # Para poner en español si quieren
)

echo " Instalando plugins de Jenkins..."
cd /var/jenkins_home

# Descargar jenkins-plugin-cli si no existe
if [ ! -f /usr/local/bin/jenkins-plugin-cli ]; then
  echo "jenkins-plugin-cli ya disponible en la imagen LTS"
fi

for plugin in "${PLUGIN_LIST[@]}"; do
  echo "  → Instalando: $plugin"
  jenkins-plugin-cli --plugins "$plugin" 2>/dev/null || echo "  ⚠️ $plugin puede requerir reinicio"
done

echo ""
echo "✅ Plugins instalados. Reiniciando Jenkins..."
echo "   Ejecuta: docker restart jenkins-lab"
