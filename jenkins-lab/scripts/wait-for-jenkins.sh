#!/usr/bin/env bash

set -euo pipefail

jenkins_url="${JENKINS_URL:-http://localhost:9090}"
auth="${JENKINS_AUTH:-admin:jenkinsadmin2026}"

for attempt in $(seq 1 60); do
    if curl -fsS -u "$auth" "$jenkins_url/login" >/dev/null 2>&1; then
        echo "Jenkins responde en $jenkins_url"
        exit 0
    fi
    sleep 5
done

echo "Jenkins no estuvo listo a tiempo" >&2
exit 1