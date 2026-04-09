#!/usr/bin/env bash

set -euo pipefail

LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_DIR="$LAB_ROOT/.work/demo-repo"
TEMPLATE_DIR="$LAB_ROOT/repo-template"

repo_owner="${GITEA_REPO_OWNER:-alumno}"
repo_password="${GITEA_REPO_PASSWORD:-alumno2026}"
repo_name="${GITEA_REPO_NAME:-jenkins-python-lab}"
remote_url="http://${repo_owner}:${repo_password}@localhost:3000/${repo_owner}/${repo_name}.git"

jenkins_url="${JENKINS_URL:-http://localhost:9090}"
jenkins_auth="${JENKINS_AUTH:-admin:jenkinsadmin2026}"
job_name="${JENKINS_JOB_NAME:-jenkins-python-lab}"

wait_for_job_visibility() {
    for attempt in $(seq 1 60); do
        if curl -fsS -u "$jenkins_auth" "$jenkins_url/job/$job_name/api/json" >/dev/null 2>&1; then
            return 0
        fi
        sleep 3
    done

    echo "El job $job_name no apareció en Jenkins" >&2
    return 1
}

current_next_build_number() {
    local payload
    payload="$(curl -fsS -u "$jenkins_auth" "$jenkins_url/job/$job_name/api/json?tree=nextBuildNumber")"
    PAYLOAD="$payload" python3 - <<'PY'
import json
import os

payload = json.loads(os.environ['PAYLOAD'])
print(payload['nextBuildNumber'])
PY
}

wait_for_build_result() {
    local expected="$1"
    local minimum_build="$2"
    local timeout_seconds="${3:-240}"
    local deadline=$((SECONDS + timeout_seconds))

    while (( SECONDS < deadline )); do
        local payload
        payload="$(curl -fsS -u "$jenkins_auth" "$jenkins_url/job/$job_name/api/json")"
        local result
        local building
        local build_number

        result="$(PAYLOAD="$payload" python3 - <<'PY'
import json
import os

payload = json.loads(os.environ['PAYLOAD'])
last_build = payload.get('lastBuild')
if not last_build:
    print('NONE')
else:
    print(last_build['number'])
PY
)"

        if [[ "$result" != "NONE" ]] && (( result >= minimum_build )); then
            local build_payload
            build_payload="$(curl -fsS -u "$jenkins_auth" "$jenkins_url/job/$job_name/lastBuild/api/json")"
            building="$(PAYLOAD="$build_payload" python3 - <<'PY'
import json
import os

print(json.loads(os.environ['PAYLOAD'])['building'])
PY
)"
            build_number="$(PAYLOAD="$build_payload" python3 - <<'PY'
import json
import os

print(json.loads(os.environ['PAYLOAD'])['number'])
PY
)"

            if [[ "$building" == "False" ]]; then
                local build_result
                build_result="$(PAYLOAD="$build_payload" python3 - <<'PY'
import json
import os

print(json.loads(os.environ['PAYLOAD'])['result'])
PY
)"

                if [[ "$build_result" == "$expected" ]]; then
                    echo "$build_number"
                    return 0
                fi
            fi
        fi
        sleep 5
    done

    echo "No se obtuvo resultado ${expected} para $job_name" >&2
    return 1
}

prepare_workdir() {
    rm -rf "$WORK_DIR"
    mkdir -p "$WORK_DIR"
    cp -R "$TEMPLATE_DIR"/. "$WORK_DIR"/
    cd "$WORK_DIR"
    git init -b main
    git config user.name 'Jenkins Lab Bot'
    git config user.email 'bot@jenkins-lab.local'
    git remote add origin "$remote_url"
}

introduce_bug() {
    python3 - <<'PY'
from pathlib import Path

path = Path('src/gradebook/mariadb_repository.py')
text = path.read_text()
old = 'WHERE student_name = %s'
new = 'WHERE module_name = %s'

if old not in text:
    raise SystemExit('No se encontró la línea esperada para introducir el bug')

path.write_text(text.replace(old, new, 1))
PY
}

fix_bug() {
    python3 - <<'PY'
from pathlib import Path

path = Path('src/gradebook/mariadb_repository.py')
text = path.read_text()
old = 'WHERE module_name = %s'
new = 'WHERE student_name = %s'

if old not in text:
    raise SystemExit('No se encontró la línea buggy para reparar')

path.write_text(text.replace(old, new, 1))
PY
}

prepare_workdir
wait_for_job_visibility

first_expected_build="$(current_next_build_number)"

introduce_bug
git add .
git commit -m 'feat: publish initial pipeline demo with failing integration adapter'
git push --force origin main

failed_build="$(wait_for_build_result FAILURE "$first_expected_build" 360)"
echo "Build con fallo verificado: ${failed_build}"

second_expected_build="$((failed_build + 1))"

fix_bug
git add src/gradebook/mariadb_repository.py
git commit -m 'fix: repair mariadb filter in integration adapter'
git push origin main

successful_build="$(wait_for_build_result SUCCESS "$second_expected_build" 360)"
echo "Build reparado y verificado: ${successful_build}"

echo "FAIL_BUILD=${failed_build}"
echo "SUCCESS_BUILD=${successful_build}"