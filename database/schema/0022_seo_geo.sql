-- =====================================================================
-- 0022  seo module : SEO & GEO Center, phase 1
--
-- GEO (generative engine optimisation) = being read, understood and
-- cited by AI engines (ChatGPT, Claude, Perplexity, Gemini, Copilot).
--
-- seo_settings gains the GEO switches (llms.txt, Markdown copies, video
-- key moments) and IndexNow (tells Bing and others about changed pages).
-- ai_bots: which AI crawler may read the site, written into robots.txt.
-- referral_visits_daily: visits that arrive from a search engine, an AI
-- engine or a social site (cookie-free, counted per day and page).
-- seo_change_log: every SEO / GEO change (by an admin or automatic),
-- with the old values so an admin can undo it.
-- =====================================================================

ALTER TABLE seo_settings
  ADD COLUMN geo_site_summary      VARCHAR(500) NOT NULL DEFAULT '' COMMENT 'one or two sentences about the site for AI engines (llms.txt), empty = default_description' AFTER robots_txt_extra,
  ADD COLUMN geo_llms_details      TEXT         NULL COMMENT 'extra Markdown for llms.txt, under the summary' AFTER geo_site_summary,
  ADD COLUMN geo_llms_enabled      TINYINT(1)   NOT NULL DEFAULT 1 COMMENT 'write llms.txt' AFTER geo_llms_details,
  ADD COLUMN geo_llms_full_enabled TINYINT(1)   NOT NULL DEFAULT 1 COMMENT 'write llms-full.txt (every course and lesson in one file)' AFTER geo_llms_enabled,
  ADD COLUMN geo_markdown_copies   TINYINT(1)   NOT NULL DEFAULT 1 COMMENT 'write /course.md, /course/lesson.md and /page.md' AFTER geo_llms_full_enabled,
  ADD COLUMN geo_video_moments     TINYINT(1)   NOT NULL DEFAULT 1 COMMENT 'VideoObject + Clip JSON-LD from video timestamps' AFTER geo_markdown_copies,
  ADD COLUMN indexnow_enabled      TINYINT(1)   NOT NULL DEFAULT 0 COMMENT 'send changed pages to IndexNow after each build' AFTER geo_video_moments,
  ADD COLUMN indexnow_key          VARCHAR(64)  NOT NULL DEFAULT '' COMMENT 'published as /<key>.txt' AFTER indexnow_enabled,
  ADD COLUMN indexnow_last_at      DATETIME(6)  NULL AFTER indexnow_key,
  ADD COLUMN indexnow_last_result  VARCHAR(300) NOT NULL DEFAULT '' AFTER indexnow_last_at;


CREATE TABLE ai_bots (
  id          BIGINT       NOT NULL AUTO_INCREMENT,
  user_agent  VARCHAR(60)  NOT NULL COMMENT 'the robots.txt User-agent token, e.g. GPTBot',
  owner       VARCHAR(60)  NOT NULL DEFAULT '',
  purpose     ENUM('training','search','user') NOT NULL COMMENT 'training = model training, search = AI search index, user = fetches a page a person asked about',
  allowed     TINYINT(1)   NOT NULL DEFAULT 1,
  notes       VARCHAR(300) NOT NULL DEFAULT '',
  sort_order  INT          NOT NULL DEFAULT 0,
  -- record controls
  is_active   TINYINT(1)   NOT NULL DEFAULT 1,
  created_at  DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at  DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by  BIGINT       NULL,
  updated_by  BIGINT       NULL,
  deleted_at  DATETIME(6)  NULL,
  deleted_by  BIGINT       NULL,
  alive       TINYINT(1)   NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY uq_ai_bots_user_agent (user_agent, alive),
  CONSTRAINT fk_ai_bots_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_ai_bots_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_ai_bots_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_ai_bots_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- All allowed at first, as before (robots.txt let every bot in). The admin decides.
INSERT INTO ai_bots (user_agent, owner, purpose, sort_order, notes) VALUES
  ('OAI-SearchBot',      'OpenAI',      'search',   10, 'ChatGPT search results'),
  ('Claude-SearchBot',   'Anthropic',   'search',   20, 'Claude search results'),
  ('PerplexityBot',      'Perplexity',  'search',   30, 'Perplexity answers'),
  ('ChatGPT-User',       'OpenAI',      'user',     40, 'Opens a page a ChatGPT user asked about'),
  ('Claude-User',        'Anthropic',   'user',     50, 'Opens a page a Claude user asked about'),
  ('Perplexity-User',    'Perplexity',  'user',     60, 'Opens a page a Perplexity user asked about'),
  ('GPTBot',             'OpenAI',      'training', 70, 'Training of OpenAI models'),
  ('ClaudeBot',          'Anthropic',   'training', 80, 'Training of Claude models'),
  ('Google-Extended',    'Google',      'training', 90, 'Gemini training and grounding (not Google Search)'),
  ('Applebot-Extended',  'Apple',       'training', 100, 'Apple Intelligence training (not Siri or Spotlight search)'),
  ('Meta-ExternalAgent', 'Meta',        'training', 110, 'Meta AI training'),
  ('CCBot',              'Common Crawl','training', 120, 'Open web archive used by many AI models'),
  ('Bytespider',         'ByteDance',   'training', 130, 'ByteDance AI training');


CREATE TABLE referral_visits_daily (
  day     DATE         NOT NULL,
  kind    ENUM('search','ai','social') NOT NULL,
  source  VARCHAR(40)  NOT NULL COMMENT 'e.g. Google, ChatGPT, LinkedIn',
  path    VARCHAR(255) NOT NULL COMMENT 'the page the visit landed on',
  visits  INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (day, kind, source, path),
  KEY ix_referral_visits_daily_source (kind, source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE seo_change_log (
  id          BIGINT       NOT NULL AUTO_INCREMENT,
  created_at  DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  actor       ENUM('admin','auto') NOT NULL COMMENT 'auto = done by the site itself (builds, GEO tasks)',
  user_id     BIGINT       NULL,
  area        VARCHAR(40)  NOT NULL COMMENT 'settings, page, ai_bot, build, indexnow',
  target      VARCHAR(255) NOT NULL DEFAULT '' COMMENT 'what changed, e.g. a path or a bot name',
  target_id   BIGINT       NULL,
  summary     VARCHAR(500) NOT NULL DEFAULT '',
  changes     JSON         NULL COMMENT 'list of {field, old, new}, used to undo',
  undone_at   DATETIME(6)  NULL,
  undone_by   BIGINT       NULL,
  PRIMARY KEY (id),
  KEY ix_seo_change_log_created (created_at),
  KEY ix_seo_change_log_area (area, target_id),
  CONSTRAINT fk_seo_change_log_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_seo_change_log_undone_by FOREIGN KEY (undone_by) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
