#!/usr/bin/env bash
# Manual deploy over SSH, from the repository folder:
#   bash deploy/cpanel/deploy_backend.sh
# Pushes to main deploy automatically (see README); use this only without GitHub Actions.
set -euo pipefail

cd "$(dirname "$0")/../.."
git pull --ff-only
bash deploy/cpanel/release.sh
