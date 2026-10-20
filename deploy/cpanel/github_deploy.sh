#!/usr/bin/env bash
# Run by GitHub Actions after a push to main: asks cPanel to pull the "deploy" branch
# and run .cpanel.yml, waits for the result and prints the server's deploy log.
# Needs CPANEL_HOST, CPANEL_USER, CPANEL_TOKEN (an API token) and CPANEL_REPO_ROOT.
set -euo pipefail

if [ -z "${CPANEL_TOKEN:-}" ]; then
  echo "::notice::CPANEL_TOKEN is not set, so nothing was deployed (see deploy/cpanel/README.md)"
  exit 0
fi
for name in CPANEL_HOST CPANEL_USER CPANEL_REPO_ROOT; do
  if [ -z "${!name:-}" ]; then
    echo "::error::$name is empty: add it in GitHub Settings > Secrets and variables > Actions"
    exit 1
  fi
done

api() {  # api Module/function [--data-urlencode name=value ...] -> prints .data
  local call=$1 reply
  shift
  reply=$(curl -fsS --get -H "Authorization: cpanel $CPANEL_USER:$CPANEL_TOKEN" \
    "https://$CPANEL_HOST:2083/execute/$call" "$@")
  if [ "$(jq -r .status <<<"$reply")" != 1 ]; then
    echo "cPanel $call failed: $(jq -c .errors <<<"$reply")" >&2
    return 1
  fi
  jq .data <<<"$reply"
}

repo=(--data-urlencode "repository_root=$CPANEL_REPO_ROOT")

echo "Pulling the deploy branch on the server"
api VersionControl/update "${repo[@]}" --data-urlencode branch=deploy > /dev/null

echo "Running .cpanel.yml"
deploy_id=$(api VersionControlDeployment/create "${repo[@]}" | jq -r .deploy_id)

state=running
for _ in $(seq 120); do  # up to 10 minutes
  sleep 5
  deployment=$(api VersionControlDeployment/retrieve |
    jq --arg id "$deploy_id" '.[] | select((.deploy_id | tostring) == $id)')
  state=$(jq -r '.timestamps | if .succeeded then "succeeded" elif .failed then "failed"
    elif .canceled then "canceled" else "running" end' <<<"$deployment")
  [ "$state" != running ] && break
done

log=$(jq -r .log_path <<<"$deployment")
echo "--- server log ($log)"
api Fileman/get_file_content --data-urlencode "dir=$(dirname "$log")" \
  --data-urlencode "file=$(basename "$log")" | jq -r .content || true
echo "--- deployment $state"
[ "$state" = succeeded ]
