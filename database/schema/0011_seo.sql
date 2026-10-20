-- =====================================================================
-- 0011  seo module : seo_settings, seo_pages, page_views_daily
--
-- Every public page gets its title, description, robots, canonical,
-- Open Graph, Twitter and JSON-LD tags from the server, so the admin can
-- change any of them in Admin -> SEO without a new release.
--   seo_settings  site-wide defaults (one row)
--   seo_pages     per-page settings, found by URL path (fixed pages such as
--                 /courses) or by the course, lesson or post a page shows
--                 (so they follow a slug change)
-- Empty text and NULL mean "automatic": the value comes from the content
-- (course title, lesson summary...) or from seo_settings.
-- =====================================================================

CREATE TABLE seo_settings (
  id                       TINYINT      NOT NULL DEFAULT 1,
  site_name                VARCHAR(60)  NOT NULL DEFAULT 'ainolez',
  title_template           VARCHAR(100) NOT NULL DEFAULT '{title} · ainolez' COMMENT 'for automatic titles, {title} is replaced',
  default_description      VARCHAR(300) NOT NULL DEFAULT '',
  default_keywords         VARCHAR(500) NOT NULL DEFAULT '',
  default_image_url        VARCHAR(500) NOT NULL DEFAULT '' COMMENT 'share image when a page has none, 1200x630',
  locale                   VARCHAR(10)  NOT NULL DEFAULT 'en_US',
  twitter_site             VARCHAR(50)  NOT NULL DEFAULT '' COMMENT '@handle',
  facebook_app_id          VARCHAR(50)  NOT NULL DEFAULT '',
  google_site_verification VARCHAR(100) NOT NULL DEFAULT '',
  bing_site_verification   VARCHAR(100) NOT NULL DEFAULT '',
  organization_logo_url    VARCHAR(500) NOT NULL DEFAULT '',
  social_profiles          JSON         NOT NULL COMMENT 'profile URLs for the Organization JSON-LD',
  allow_indexing           TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '0 on staging: every page is noindex and robots.txt blocks all',
  robots_txt_extra         TEXT         NULL COMMENT 'extra lines appended to robots.txt',
  last_build_at            DATETIME(6)  NULL COMMENT 'last prerender + sitemap build',
  last_build_pages         INT          NOT NULL DEFAULT 0,
  updated_at               DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  updated_by               BIGINT       NULL,
  PRIMARY KEY (id),
  CONSTRAINT ck_seo_settings_single CHECK (id = 1),
  CONSTRAINT fk_seo_settings_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO seo_settings (id, default_description, default_keywords, social_profiles) VALUES (1,
  'Free coding and AI courses, a live code editor, and an AI tutor, for everyone.',
  'learn coding, free courses, python, ai, html, css, javascript, sql, tutorials',
  '[]');


-- A row has either a path (fixed or custom page) or an entity (course,
-- lesson or community post), never both.
CREATE TABLE seo_pages (
  id                 BIGINT        NOT NULL AUTO_INCREMENT,
  path               VARCHAR(255)  NULL COMMENT 'e.g. /courses, for pages that are not a course, lesson or post',
  entity_type        ENUM('course', 'lesson', 'post') NULL,
  entity_id          BIGINT        NULL,
  meta_title         VARCHAR(200)  NOT NULL DEFAULT '' COMMENT 'used exactly as typed (no template)',
  meta_description   VARCHAR(300)  NOT NULL DEFAULT '',
  keywords           VARCHAR(500)  NOT NULL DEFAULT '',
  canonical_url      VARCHAR(500)  NOT NULL DEFAULT '',
  robots             ENUM('index,follow', 'noindex,follow', 'index,nofollow', 'noindex,nofollow') NULL,
  og_title           VARCHAR(200)  NOT NULL DEFAULT '',
  og_description     VARCHAR(300)  NOT NULL DEFAULT '',
  og_image_url       VARCHAR(500)  NOT NULL DEFAULT '',
  og_type            VARCHAR(30)   NOT NULL DEFAULT '',
  twitter_card       ENUM('summary', 'summary_large_image') NULL,
  structured_data    JSON          NULL COMMENT 'extra JSON-LD object or list added to the page',
  in_sitemap         TINYINT(1)    NOT NULL DEFAULT 1,
  sitemap_priority   DECIMAL(2,1)  NULL,
  sitemap_changefreq ENUM('always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never') NULL,
  -- record controls
  is_active          TINYINT(1)    NOT NULL DEFAULT 1,
  created_at         DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at         DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by         BIGINT        NULL,
  updated_by         BIGINT        NULL,
  deleted_at         DATETIME(6)   NULL,
  deleted_by         BIGINT        NULL,
  alive              TINYINT(1)    NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY uq_seo_pages_path (path, alive),
  UNIQUE KEY uq_seo_pages_entity (entity_type, entity_id, alive),
  CONSTRAINT ck_seo_pages_target CHECK (
    (path IS NOT NULL AND entity_type IS NULL AND entity_id IS NULL)
    OR (path IS NULL AND entity_type IS NOT NULL AND entity_id IS NOT NULL)
  ),
  CONSTRAINT fk_seo_pages_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_seo_pages_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_seo_pages_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_seo_pages_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- The fixed pages of the website, ready for the admin to edit.
INSERT INTO seo_pages (path, meta_title, meta_description, robots, in_sitemap, sitemap_priority, sitemap_changefreq) VALUES
  ('/',                'ainolez · Learn it. Code it. Own it.',
                       'Free coding and AI courses with a live code editor, quizzes, certificates and an AI tutor. Learn Python, AI, HTML, CSS, JavaScript and SQL.',
                       NULL, 1, 1.0, 'daily'),
  ('/courses',         'Free coding and AI courses · ainolez',
                       'Browse every free ainolez course: Python, artificial intelligence, machine learning, web development and SQL, from beginner to advanced.',
                       NULL, 1, 0.9, 'weekly'),
  ('/community',       'Community · ainolez',
                       'Ask questions, share projects and help other learners in the free ainolez community.',
                       NULL, 1, 0.6, 'daily'),
  ('/ai',              'AI tutor · ainolez',
                       'Ask the free ainolez AI tutor about any lesson, your code or a concept you are learning.',
                       NULL, 1, 0.6, 'monthly'),
  ('/leaderboard',     'Leaderboard · ainolez',
                       'The learners who earned the most ainolez points this week, this month and of all time.',
                       NULL, 1, 0.3, 'daily'),
  ('/search',          'Search lessons · ainolez', '', 'noindex,follow', 0, NULL, NULL),
  ('/login',           'Log in · ainolez', 'Log in to ainolez to continue your free courses.', 'noindex,follow', 0, NULL, NULL),
  ('/register',        'Sign up free · ainolez',
                       'Create a free ainolez account to track your progress, earn points and get certificates.',
                       NULL, 1, 0.5, 'yearly'),
  ('/forgot-password', 'Forgot password · ainolez', '', 'noindex,follow', 0, NULL, NULL),
  ('/reset-password',  'Reset password · ainolez',  '', 'noindex,nofollow', 0, NULL, NULL),
  ('/verify-email',    'Verify email · ainolez',    '', 'noindex,nofollow', 0, NULL, NULL);

-- Lessons had their own SEO title and description (0004). They move here.
INSERT INTO seo_pages (entity_type, entity_id, meta_title, meta_description)
SELECT 'lesson', id, seo_title, seo_description
FROM lessons
WHERE deleted_at IS NULL AND (seo_title <> '' OR seo_description <> '');

ALTER TABLE lessons DROP COLUMN seo_title, DROP COLUMN seo_description;


-- Cookie-free analytics: the website asks for a page's SEO tags on every
-- page view, which also counts the view here.
CREATE TABLE page_views_daily (
  day   DATE         NOT NULL,
  path  VARCHAR(255) NOT NULL,
  views INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (day, path),
  KEY ix_page_views_daily_path (path)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
