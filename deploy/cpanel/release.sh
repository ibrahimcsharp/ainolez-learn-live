#!/usr/bin/env bash
# Makes the code in this checkout live. Runs on the server after new code arrives:
# from .cpanel.yml (automatic deploys from GitHub) or from deploy_backend.sh (SSH).
#   1. installs Python packages      2. backs up the database
#   3. applies new SQL files and seeds new starter courses
#   4. publishes the website build (frontend/dist, if present) and rebuilds SEO pages
#   5. restarts the API
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
VENV="${VENV:-$HOME/virtualenv/apps/ainolez/backend/3.11}"
SITE="${SITE:-$HOME/public_html}"
PYTHON="$VENV/bin/python"
export DJANGO_SETTINGS_MODULE=config.settings.production

# Copy all output to ~/deploy.log. (exec > >(tee) needs /dev/fd, which cPanel's CageFS lacks.)
if [ -z "${RELEASE_LOGGED:-}" ]; then
  RELEASE_LOGGED=1 bash "$0" "$@" 2>&1 | tee -a "$HOME/deploy.log"
  exit "${PIPESTATUS[0]}"
fi

echo "=== $(date '+%F %T') deploying $(git -C "$REPO" rev-parse --short HEAD)"
cd "$REPO/backend"

"$PYTHON" -m pip install --quiet -r requirements.txt

# Back up before the schema changes; keep the 10 newest backups.
env_value() { grep -E "^$1=" .env | cut -d= -f2- | tr -d '\r' | sed 's/[[:space:]]*$//'; }
mkdir -p tmp "$HOME/backups"
backup="$HOME/backups/before-deploy-$(date +%Y%m%d-%H%M%S).sql.gz"
MYSQL_PWD="$(env_value DB_PASSWORD)" mysqldump -u "$(env_value DB_USER)" "$(env_value DB_NAME)" | gzip > "$backup"
ls -1t "$HOME"/backups/before-deploy-*.sql.gz | tail -n +11 | xargs -r rm --

"$PYTHON" manage.py apply_schema
"$PYTHON" manage.py migrate --noinput
"$PYTHON" manage.py seed_courses   # adds only courses that do not exist yet

if [ -d "$REPO/frontend/dist" ]; then
  cp -R "$REPO/frontend/dist/." "$SITE/"
  "$PYTHON" manage.py seo_build      # the copy replaced index.html with the plain app
fi

touch tmp/restart.txt                # Passenger reloads the app (CGI needs nothing)
echo "=== done, backup: $backup"
