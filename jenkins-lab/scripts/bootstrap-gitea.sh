#!/usr/bin/env bash

set -euo pipefail

LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$LAB_ROOT"

gitea_url="${GITEA_URL:-http://localhost:3000}"
repo_owner="${GITEA_REPO_OWNER:-alumno}"
repo_password="${GITEA_REPO_PASSWORD:-alumno2026}"
repo_name="${GITEA_REPO_NAME:-jenkins-python-lab}"
webhook_url="${JENKINS_NOTIFY_URL:-http://webhook-relay:8081/gitea/push}"

wait_for_gitea() {
    for attempt in $(seq 1 60); do
        if curl -fsS "$gitea_url/api/healthz" >/dev/null 2>&1; then
            echo "Gitea responde en $gitea_url"
            return 0
        fi
        sleep 3
    done

    echo "Gitea no estuvo lista a tiempo" >&2
    return 1
}

ensure_user() {
    local username="$1"
    local password="$2"
    local email="$3"
    local extra_args=()

    if [[ "${4:-}" == "admin" ]]; then
        extra_args+=(--admin)
    fi

    if docker compose exec -T --user git gitea gitea admin user list | grep -q "${username}"; then
        echo "Usuario ${username} ya existe"
        return 0
    fi

    docker compose exec -T --user git gitea gitea admin user create \
        --username "$username" \
        --password "$password" \
        --email "$email" \
        --must-change-password=false \
        "${extra_args[@]}"
}

ensure_repo() {
    local status
    status="$(curl -s -o /dev/null -w '%{http_code}' -u "$repo_owner:$repo_password" "$gitea_url/api/v1/repos/$repo_owner/$repo_name")"

    if [[ "$status" == "200" ]]; then
        echo "Repositorio ${repo_owner}/${repo_name} ya existe"
        return 0
    fi

    curl -fsS -u "$repo_owner:$repo_password" \
        -H 'Content-Type: application/json' \
        -d "{\"name\":\"${repo_name}\",\"private\":false,\"default_branch\":\"main\"}" \
        "$gitea_url/api/v1/user/repos" >/dev/null

    echo "Repositorio ${repo_owner}/${repo_name} creado"
}

ensure_webhook() {
    local hooks_json
    local existing_ids

    hooks_json="$(curl -fsS -u "$repo_owner:$repo_password" "$gitea_url/api/v1/repos/$repo_owner/$repo_name/hooks")"
    existing_ids="$(HOOKS_JSON="$hooks_json" TARGET_URL="$webhook_url" python3 - <<'PY'
import json
import os

hooks = json.loads(os.environ['HOOKS_JSON'])
target = os.environ['TARGET_URL']
for hook in hooks:
    if hook.get('config', {}).get('url') == target:
        print(hook['id'])
PY
)"

    if [[ -n "$existing_ids" ]]; then
        while IFS= read -r hook_id; do
            [[ -z "$hook_id" ]] && continue
            curl -fsS -u "$repo_owner:$repo_password" -X DELETE \
                "$gitea_url/api/v1/repos/$repo_owner/$repo_name/hooks/$hook_id" >/dev/null
        done <<< "$existing_ids"
    fi

    curl -fsS -u "$repo_owner:$repo_password" \
        -H 'Content-Type: application/json' \
        -d "{\"active\":true,\"branch_filter\":\"\",\"config\":{\"content_type\":\"json\",\"url\":\"${webhook_url}\",\"http_method\":\"get\"},\"events\":[\"push\"],\"type\":\"gitea\"}" \
        "$gitea_url/api/v1/repos/$repo_owner/$repo_name/hooks" >/dev/null

    echo "Webhook creado hacia ${webhook_url}"
}

wait_for_gitea
ensure_user "$repo_owner" "$repo_password" "${repo_owner}@jenkins-lab.local"
ensure_repo
ensure_webhook