#!/usr/bin/env bash

set -euo pipefail

LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$LAB_ROOT"

docker compose down -v --remove-orphans
docker compose up -d --build

"$LAB_ROOT/scripts/wait-for-jenkins.sh"
"$LAB_ROOT/scripts/bootstrap-gitea.sh"
"$LAB_ROOT/scripts/run-demo.sh"