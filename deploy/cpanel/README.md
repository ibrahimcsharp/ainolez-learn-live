# Deploying ainolez to cPanel

Two parts: the React build goes to `public_html/`, the Django API runs as a
Passenger app on `api.<domain>`.

## One-time setup

1. **Database** (cPanel → MySQL Databases): create a database and a user, give the
   user *All privileges* on it.
2. **Code**: `git clone` the repository to `~/apps/ainolez` (outside `public_html`).
3. **Python app** (cPanel → Setup Python App → Create):
   - Python 3.11, application root `apps/ainolez/backend`, URL `api.<domain>`
   - startup file `passenger_wsgi.py`, entry point `application`
4. **Settings**: copy `backend/.env.example` to `backend/.env`, fill it in, `chmod 600 .env`.
   Leave `DB_ENGINE` out (the server's MySQL/MariaDB is new enough).
   - `FRONTEND_URL` must be the website's address: the Try-it sandbox page
     (`api.<domain>/runner/`) only lets that site embed it.
   - `PRERENDER_DIR` is the website folder, e.g. `/home/<user>/public_html`. The API
     writes the prerendered pages, `sitemap.xml` and `robots.txt` there.
5. **Tables and admin** (SSH, inside the app's virtualenv, in `backend/`):
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings.production
   pip install -r requirements.txt
   python manage.py apply_schema
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py seed_courses        # the 16 starter courses, published
   ```
   The MySQL driver is PyMySQL (pure Python), so nothing needs compiling. If
   mysqlclient happens to be installed it is used instead (`config/__init__.py`).
6. **Cron** (cPanel → Cron Jobs), replace the paths with yours:
   ```
   * * * * *  cd ~/apps/ainolez/backend && ~/virtualenv/apps/ainolez/backend/3.11/bin/python manage.py run_jobs --settings=config.settings.production >> tmp/cron.log 2>&1
   0 2 * * *  cd ~/apps/ainolez/backend && ~/virtualenv/apps/ainolez/backend/3.11/bin/python manage.py ai_nightly --settings=config.settings.production >> tmp/cron.log 2>&1
   30 2 * * * cd ~/apps/ainolez/backend && ~/virtualenv/apps/ainolez/backend/3.11/bin/python manage.py seo_build --settings=config.settings.production >> tmp/cron.log 2>&1
   0 3 * * *  mysqldump -u USER -p'PASSWORD' DBNAME | gzip > ~/backups/ainolez-$(date +\%a).sql.gz
   ```
   `ai_nightly` re-indexes the AI tutor's knowledge and deletes chats older than the
   retention period. `seo_build` rewrites the prerendered pages, sitemap and robots.txt
   (content changes already trigger a rebuild a minute later through `run_jobs`; the
   nightly run is a safety net). The backup line keeps one file per weekday, so seven days are kept.
7. **AI tutor**: put `ANTHROPIC_API_KEY` in `.env`, then use *Test connection* in
   Admin → AI tutor. The host must allow outbound HTTPS to api.anthropic.com.

## Every release

- **API**: `bash deploy/cpanel/deploy_backend.sh` (backs up the database, applies new
  SQL files, restarts Passenger).
- **Website**: on your PC, `cd frontend`, create `.env` with
  `VITE_API_URL=https://api.<domain>/api/v1`, run `npm run build`, then upload the
  contents of `frontend/dist/` (including `.htaccess` and `shell.html`) to `public_html/`.
  The upload replaces `index.html` with the plain app, so then run
  `python manage.py seo_build` on the server (or press *Rebuild now* in Admin → SEO)
  to write the prerendered pages again. The build adds a strict Content-Security-Policy
  to the page; if you add a new outside service (a CDN, an embed), add it to
  `contentSecurityPolicy` in `frontend/vite.config.js`.

## Checks after deploying

- `https://api.<domain>/api/v1/health/` returns `{"status": "ok"}`.
- Opening `https://<domain>/login` directly (not via a link) loads the page.
- `tmp/cron.log` shows `run_jobs` running and the sign-up email arrives.
- `https://<domain>/sitemap.xml` lists the courses, and *View source* on a course page
  shows its title and description in the HTML.
- A Try-it example runs on a lesson page (Python, SQL and an HTML example), and the
  browser console shows no Content-Security-Policy errors.
- Logging in with a wrong password many times in a row is answered with
  "Request was throttled" (rate limits keep their counters in `tmp/cache`, or `CACHE_DIR`).
