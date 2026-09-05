#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi
: "${DEMAND_REPO:=KingCrimsonD/octo-cli-pm-agent-lab}"
export DEMAND_REPO
python3 scripts/scan_github_issues.py
