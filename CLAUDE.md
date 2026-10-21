# ainolez

Free coding and AI learning platform. Full plan, diagrams and database design:
`docs/PLANNING.md`. Slogan: "Learn it. Code it. Own it."

## Layout
- `database/` — hand-written MySQL. `00_create_databases.sql` (run once as root),
  `schema/NNNN_*.sql` applied in order by `manage.py apply_schema`.
- `backend/` — Django 5.2 + DRF modular monolith.
  `shared/` kernel (BaseModel with soft delete, audit, jobs, SQL loader),
  `modules/<name>/` (models, services, selectors, api/, admin_api/, tasks, tests).
- `frontend/` — React 18 + Vite. `app/` (router, auth, layouts), `shared/` (api client,
  ui, styles), `features/<area>/`.
- `deploy/cpanel/` — server setup and release script.

## Rules
- **SQL is the source of truth.** Every table is created by a new numbered file in
  `database/schema/` and mapped with `managed = False` models. Never edit an applied
  file; add the next number (e.g. ALTER TABLE in `0003_...sql`). Django `migrate` only
  creates its own framework tables.
- No semicolons inside SQL strings (the loader splits on `;`).
- Business logic lives in `services.py`; reads in `selectors.py`; views stay thin.
- A module uses another module only through its `services`, `selectors` or `events`
  (enforced by `shared/tests/test_module_boundaries.py`).
- Manageable tables carry the record-control columns: is_active, created/updated_at/by,
  deleted_at/by, alive (`UNIQUE(x, alive)` keeps soft-deleted rows from blocking reuse).
- Slow work (emails, AI, PDFs) goes through `shared.jobs.enqueue`; cron runs `run_jobs`.
- Admin resources subclass `AdminResourceViewSet`; create/edit go through the module's
  `save_*` service. Lesson block HTML is sanitised on save, so the frontend can insert it.
- Tests that need committed rows (FULLTEXT search) use the `committed_db` fixture.
- Modules react to each other through events (`learning/events.py`), never by calling
  into each other's services. Handlers run inside the publisher's transaction.
- Public assessment data (`assessment/selectors.*_for_learner`) must never include
  answers, solutions or expected values.
- Only `modules/assistant/claude.py` may import `anthropic`. Tests replace
  `claude.complete` (see assistant/tests) so they never call the API.
- Course slugs are top-level URLs (`/python`); `RESERVED_SLUGS` in catalog/services.py
  must list every fixed frontend route. Site pages (`website` module) share those URLs:
  each module refuses a slug the other uses.
- Code must run on Python 3.11 (cPanel) and MariaDB 10.4 (local XAMPP, via
  `config/db/mariadb104`).

## Local commands (Windows, XAMPP MySQL running)
```
cd backend
.venv\Scripts\python manage.py apply_schema
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py runserver
.venv\Scripts\python manage.py run_jobs --watch   # sends queued emails (printed to console)
.venv\Scripts\python -m pytest
.venv\Scripts\python -m ruff check . ; .venv\Scripts\python -m ruff format .

cd frontend
npm run dev     # http://localhost:5173, proxies /api to :8000
npm test
npm run build
```

## Progress
- [x] Sprint 1: brand + tokens, layouts (public, learner, admin), shared kernel, identity
      (register, verify, login/JWT cookie, refresh, logout, reset, profile), admin
      dashboard stats, jobs + cron, CI, cPanel deploy files.
      Deferred to when first needed: event bus (Sprint 3), og-default.png and
      favicon.ico (Sprint 5 SEO).
- [x] Sprint 2: SQL 0003 (media) + 0004 (catalog); shared record controls
      (`shared/admin_api.py` + `shared/records.py`: activate, soft delete, restore, hard
      delete with preview + typed confirm, bulk, reorder); catalog CRUD (categories,
      courses, chapters, lessons, blocks, learning paths); media library; content_tools
      (Markdown → sanitised HTML, video/embed allow-list, .md/.zip import, .md export);
      admin CMS screens incl. block editor with live preview and Trash; public catalogue,
      course page, W3-style lesson page (/course/lesson), FULLTEXT search.
      Differences from PLANNING.md: nh3 instead of bleach (bleach is deprecated);
      `lessons.course_id` added so lesson slugs are unique per course; quiz/exercise
      blocks and shortcodes move to Sprint 3 with the assessment tables.
- [x] Sprint 3: SQL 0005–0008; `shared/events.py` event bus (handlers.py autodiscovered);
      assessment (exercises: exact/contains/regex/output checks; quizzes with final flag,
      graded on the server); learning (enrol, visit/resume, complete lesson, course
      completion = all lessons + final quizzes → `CourseCompleted`); gamification (rules,
      append-only ledger, streaks, badges, leaderboard with opt-out); certification (auto
      issue or review via CERTIFICATES_NEED_REVIEW, PDF + 1200×627 PNG in a job, public
      verify page, `/share/certificates/<code>/` Open Graph page for LinkedIn, revoke /
      re-issue / templates). Frontend: CodeMirror Try-it (iframe sandbox, Pyodide,
      sql.js from jsDelivr), exercise and quiz blocks, progress + Mark complete,
      course-complete dialog, learner dashboard, leaderboard, certificate share page,
      admin quiz builder, points & badges, certificates.
      Differences from PLANNING.md: quiz answers stored as JSON on `quiz_attempts`
      (no attempt_answers table); weekly/monthly points are summed from the ledger;
      badge icons are emoji; bookmarks/snippets and per-course leaderboards moved later.
      Known limits: Python runs on the page's main thread (an endless loop freezes the
      tab); the server trusts the output the browser reports for "output" exercises.
- [x] Sprint 4: SQL 0009 (community) + 0010 (assistant). Community: spaces, posts, replies,
      lesson comments, likes, reports, moderation queue (approve/reject/hide/pin/lock/ban);
      new content waits for approval unless the author has COMMUNITY_TRUSTED_POINTS and
      the space is open; first post and helpful-answer points. AI tutor: Claude via the
      `anthropic` SDK only in `assistant/claude.py` (beta stream + get_final_message,
      `fallbacks="default"`, cached system prompt, effort); RAG over `kb_chunks` FULLTEXT
      with the open lesson always included; `LessonChanged` (catalog) → index job;
      `ai_nightly` cron; curated FAQ (difflib match, no model call); daily limits,
      monthly token budget, usage + cost; prompt versions with rollback; admin control
      panel (settings, prompt, knowledge base + test search, FAQ, conversations →
      "Save as FAQ", usage, test connection). Frontend: floating chat + /ai page,
      "Ask AI" in every Try-it editor, lesson discussion, /community pages.
      Differences from PLANNING.md: knowledge sources are lessons + pasted documents
      (no PDF/URL fetching yet; URL fetching needs SSRF protection); answers are not
      streamed to the browser; no bad-word filter or AI spam pre-screen yet (Sprint 5).
      Not verified: a real Claude answer — needs ANTHROPIC_API_KEY in backend/.env.
- [x] Sprint 5: AI course generator, seed content, hardening, launch.
      SQL 0011–0014; `seo` module (every page's tags from Admin → SEO, per-path or
      per-course/lesson/post rows, site defaults, report, prerendered HTML + sitemap +
      robots via `seo_build` / PRERENDER_DIR, cookie-free page views); og-default.png,
      favicon; `ai_authoring` (outline → edit → lesson jobs, drafts only); ```exercise /
      ```quiz fences in .md import; 11 seed courses in `database/seed/courses/`
      (`seed_courses`; `test_seed_content.py` runs every exercise solution: Python, SQL,
      JavaScript via Node, regex/contains checks); Try-it runs on the API's /runner/ page
      so the build CSP stays strict; Pyodide auto-loads packages and shows matplotlib
      charts; admin Analytics (`platform_admin` analytics: page views, signups,
      enrolments, completions, top pages and courses; `shared/stats.daily_counts`);
      community blocked words (`community_settings`, hold or refuse, shown in the queue);
      rate limits: ScopedRateThrottle is the default class, scopes in base.py, counters
      in a file cache (CACHE_DIR) so all Passenger processes share them.
      Not verified: the sandboxed Try-it iframe in a real browser (the Claude browser
      pane blocks every sandboxed iframe); pandas/scikit-learn seed exercises are
      skipped by pytest unless those packages are installed.
- [x] After launch: SQL 0015 (courses.intro_video_url, shown on the course page) + 0016
      (ai_settings.course_generator_enabled, checked by ai_authoring before new work).
      Course editor: tabs (Lessons first), one "Publish course" (`POST courses/{id}/publish/`
      also publishes the draft lessons), "Add lesson" opens the new lesson; block picker
      with icons and YouTube preview; media "Copy link / Markdown", upload inside the image
      picker, "Add an image from Media" in text blocks; on/off cards for the AI tutor and
      the course generator.
      5 more Python seed courses (original text, following the W3Schools Python topic list):
      python-essentials, python-standard-library, python-oop, python-dsa, python-databases.
      CGI fallback for the API (`deploy/cpanel/cgi/`) while the host has Passenger off.
- [x] Pages and menus: SQL 0017 (`site_pages`, `menus`, `menu_items`; seo_pages.entity_type
      gains 'page'). `website` module: pages at `/<slug>` (Markdown → nh3-sanitised HTML on
      save, active/inactive, Trash + restore), header and footer menus with ordered links to a
      page, a course or a URL (0017 seeds the links that were hard-coded). Public API
      `/api/v1/public/site/menus/` and `pages/<slug>/`; `CoursePage` falls back to the page
      when no course has the slug. SEO: WebPage JSON-LD, sitemap entries, per-page SEO tab.
      Admin: Pages (smart editor `admin/shared/MarkdownEditor.jsx`: toolbar, live preview,
      image upload / paste / drop into the media library, so it works before the first save)
      and Menus (drag to reorder menus and links).
      Sub-menus: SQL 0018 (`menu_items.parent_id`, one level; link_type 'none' = a heading that
      only holds a sub-menu). Header: dropdown (`features/website/MenuDropdown.jsx`, hover or
      arrow button; on phones the panel sits under the header). Footer: indented list.
      `MenuItem.page` uses `delete_links` instead of CASCADE: Django's CASCADE first sets
      page_id to NULL on MySQL, which `ck_menu_items_target` refuses.
