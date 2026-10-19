#!/usr/bin/env bash
# Update the API on the cPanel server. Run over SSH from the repository folder:
#   bash deploy/cpanel/deploy_backend.sh
# VENV is the "source" path shown in cPanel > Setup Python App.
set -euo pipefail

VENV="${VENV:-$HOME/virtualenv/apps/ainolez/backend/3.11}"
cd "$(dirname "$0")/../../backend"

env_value() { grep -E "^$1=" .env | cut -d= -f2-; }

git pull --ff-only
source "$VENV/bin/activate"
pip install --quiet -r requirements.txt

# Back up the database before changing its schema.
mkdir -p tmp "$HOME/backups"
backup="$HOME/backups/before-deploy-$(date +%Y%m%d-%H%M).sql.gz"
mysqldump -u "$(env_value DB_USER)" -p"$(env_value DB_PASSWORD)" "$(env_value DB_NAME)" | gzip > "$backup"

export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py apply_schema
python manage.py migrate --noinput
touch tmp/restart.txt  # tells Passenger to reload the app
echo "Deployed. Backup: $backup"
