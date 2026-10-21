-- =====================================================================
-- 0017  website module : site_pages, menus, menu_items
--
--   site_pages  pages the admin writes (About, Privacy...), shown at
--               /<slug> like a course, so page and course slugs never
--               clash (checked by both modules on save)
--   menus       a named list of links placed in the header or the footer
--               (each footer menu is one footer column)
--   menu_items  the ordered links of a menu: a page, a course or a URL
-- Only active rows are shown on the website.
-- =====================================================================

CREATE TABLE site_pages (
  id           BIGINT        NOT NULL AUTO_INCREMENT,
  title        VARCHAR(200)  NOT NULL,
  slug         VARCHAR(100)  NOT NULL COMMENT 'public URL: /<slug>',
  summary      VARCHAR(300)  NOT NULL DEFAULT '' COMMENT 'search and share description',
  content_md   LONGTEXT      NULL COMMENT 'what the admin typed (Markdown)',
  content_html LONGTEXT      NULL COMMENT 'sanitised HTML the public page shows',
  -- record controls
  is_active    TINYINT(1)    NOT NULL DEFAULT 1,
  created_at   DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at   DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by   BIGINT        NULL,
  updated_by   BIGINT        NULL,
  deleted_at   DATETIME(6)   NULL,
  deleted_by   BIGINT        NULL,
  alive        TINYINT(1)    NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY uq_site_pages_slug (slug, alive),
  CONSTRAINT fk_site_pages_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_site_pages_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_site_pages_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_site_pages_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE menus (
  id          BIGINT        NOT NULL AUTO_INCREMENT,
  name        VARCHAR(100)  NOT NULL COMMENT 'footer menus show it as the column heading',
  location    ENUM('header', 'footer') NOT NULL,
  sort_order  INT           NOT NULL DEFAULT 0,
  -- record controls
  is_active   TINYINT(1)    NOT NULL DEFAULT 1,
  created_at  DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at  DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by  BIGINT        NULL,
  updated_by  BIGINT        NULL,
  deleted_at  DATETIME(6)   NULL,
  deleted_by  BIGINT        NULL,
  alive       TINYINT(1)    NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY ix_menus_location_order (location, sort_order),
  CONSTRAINT fk_menus_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_menus_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_menus_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_menus_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Exactly one target per row, matching link_type. Deleting a page or a
-- course for real removes the links to it.
CREATE TABLE menu_items (
  id              BIGINT        NOT NULL AUTO_INCREMENT,
  menu_id         BIGINT        NOT NULL,
  label           VARCHAR(100)  NOT NULL DEFAULT '' COMMENT 'blank: the page or course title',
  link_type       ENUM('page', 'course', 'url') NOT NULL,
  page_id         BIGINT        NULL,
  course_id       BIGINT        NULL,
  url             VARCHAR(500)  NOT NULL DEFAULT '' COMMENT '/path, https://... or mailto:',
  open_in_new_tab TINYINT(1)    NOT NULL DEFAULT 0,
  sort_order      INT           NOT NULL DEFAULT 0,
  -- record controls
  is_active       TINYINT(1)    NOT NULL DEFAULT 1,
  created_at      DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at      DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by      BIGINT        NULL,
  updated_by      BIGINT        NULL,
  deleted_at      DATETIME(6)   NULL,
  deleted_by      BIGINT        NULL,
  alive           TINYINT(1)    NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY ix_menu_items_menu_order (menu_id, sort_order),
  CONSTRAINT fk_menu_items_menu       FOREIGN KEY (menu_id)   REFERENCES menus (id)      ON DELETE CASCADE,
  CONSTRAINT fk_menu_items_page       FOREIGN KEY (page_id)   REFERENCES site_pages (id) ON DELETE CASCADE,
  CONSTRAINT fk_menu_items_course     FOREIGN KEY (course_id) REFERENCES courses (id)    ON DELETE CASCADE,
  CONSTRAINT fk_menu_items_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_menu_items_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_menu_items_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_menu_items_target CHECK (
    (link_type = 'page' AND page_id IS NOT NULL AND course_id IS NULL)
    OR (link_type = 'course' AND course_id IS NOT NULL AND page_id IS NULL)
    OR (link_type = 'url' AND url <> '' AND page_id IS NULL AND course_id IS NULL)
  ),
  CONSTRAINT ck_menu_items_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- The links the website had hard-coded, ready for the admin to edit.
INSERT INTO menus (id, name, location, sort_order) VALUES
  (1, 'Main menu', 'header', 0),
  (2, 'Learn',     'footer', 1),
  (3, 'Community', 'footer', 2),
  (4, 'Account',   'footer', 3);

INSERT INTO menu_items (menu_id, label, link_type, url, sort_order) VALUES
  (1, 'Courses',      'url', '/courses',     0),
  (1, 'Community',    'url', '/community',   1),
  (1, 'AI tutor',     'url', '/ai',          2),
  (1, 'Leaderboard',  'url', '/leaderboard', 3),
  (2, 'All courses',  'url', '/courses',     0),
  (2, 'Python',       'url', '/python',      1),
  (2, 'HTML',         'url', '/html',        2),
  (2, 'AI',           'url', '/intro-to-ai', 3),
  (3, 'Forum',        'url', '/community',   0),
  (3, 'Leaderboard',  'url', '/leaderboard', 1),
  (3, 'AI tutor',     'url', '/ai',          2),
  (4, 'Sign up free', 'url', '/register',    0),
  (4, 'Log in',       'url', '/login',       1),
  (4, 'My dashboard', 'url', '/dashboard',   2);


-- Page SEO is stored by the page (like courses and lessons), so it
-- follows a slug change.
ALTER TABLE seo_pages
  MODIFY entity_type ENUM('course', 'lesson', 'post', 'page') NULL;
