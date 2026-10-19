-- =====================================================================
-- 0004  catalog module : categories, courses, chapters, lessons,
--       code_examples, lesson_blocks, learning_paths, learning_path_courses
--
-- Hierarchy:  category -> course -> chapter -> lesson -> blocks
-- Deleting a parent row for real (hard delete) cascades to its children.
-- Each table repeats the record-control columns described in 0001.
-- =====================================================================

CREATE TABLE categories (
  id          BIGINT        NOT NULL AUTO_INCREMENT,
  name        VARCHAR(100)  NOT NULL,
  slug        VARCHAR(100)  NOT NULL,
  description VARCHAR(500)  NOT NULL DEFAULT '',
  icon        VARCHAR(50)   NOT NULL DEFAULT '' COMMENT 'emoji or icon name',
  color       CHAR(7)       NOT NULL DEFAULT '#04AA6D',
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
  UNIQUE KEY uq_categories_slug (slug, alive),
  CONSTRAINT fk_categories_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_categories_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_categories_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_categories_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE courses (
  id                 BIGINT        NOT NULL AUTO_INCREMENT,
  category_id        BIGINT        NOT NULL,
  title              VARCHAR(200)  NOT NULL,
  slug               VARCHAR(100)  NOT NULL COMMENT 'public URL: /<slug>',
  short_description  VARCHAR(300)  NOT NULL DEFAULT '',
  description        TEXT          NULL,
  level              ENUM('beginner', 'intermediate', 'advanced') NOT NULL DEFAULT 'beginner',
  language_key       ENUM('html', 'css', 'javascript', 'python', 'sql', 'ai', 'other') NOT NULL DEFAULT 'other',
  thumbnail_media_id BIGINT        NULL,
  estimated_minutes  INT           NOT NULL DEFAULT 0,
  status             ENUM('draft', 'published', 'archived') NOT NULL DEFAULT 'draft',
  published_at       DATETIME(6)   NULL,
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
  UNIQUE KEY uq_courses_slug (slug, alive),
  KEY ix_courses_category_status (category_id, status),
  CONSTRAINT fk_courses_category   FOREIGN KEY (category_id)        REFERENCES categories (id)  ON DELETE CASCADE,
  CONSTRAINT fk_courses_thumbnail  FOREIGN KEY (thumbnail_media_id) REFERENCES media_files (id) ON DELETE SET NULL,
  CONSTRAINT fk_courses_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_courses_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_courses_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_courses_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE chapters (
  id          BIGINT        NOT NULL AUTO_INCREMENT,
  course_id   BIGINT        NOT NULL,
  title       VARCHAR(200)  NOT NULL,
  description VARCHAR(500)  NOT NULL DEFAULT '',
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
  KEY ix_chapters_course_order (course_id, sort_order),
  CONSTRAINT fk_chapters_course     FOREIGN KEY (course_id)  REFERENCES courses (id) ON DELETE CASCADE,
  CONSTRAINT fk_chapters_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_chapters_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_chapters_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_chapters_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- course_id is copied from the chapter so a lesson slug is unique per
-- course, which gives clean URLs like /python/lists.
CREATE TABLE lessons (
  id                BIGINT        NOT NULL AUTO_INCREMENT,
  course_id         BIGINT        NOT NULL,
  chapter_id        BIGINT        NOT NULL,
  title             VARCHAR(200)  NOT NULL,
  slug              VARCHAR(100)  NOT NULL,
  summary           VARCHAR(500)  NOT NULL DEFAULT '',
  estimated_minutes INT           NOT NULL DEFAULT 5,
  status            ENUM('draft', 'published', 'archived') NOT NULL DEFAULT 'draft',
  sort_order        INT           NOT NULL DEFAULT 0,
  source_md         LONGTEXT      NULL COMMENT 'original imported Markdown',
  seo_title         VARCHAR(200)  NOT NULL DEFAULT '',
  seo_description   VARCHAR(300)  NOT NULL DEFAULT '',
  published_at      DATETIME(6)   NULL,
  -- record controls
  is_active         TINYINT(1)    NOT NULL DEFAULT 1,
  created_at        DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at        DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by        BIGINT        NULL,
  updated_by        BIGINT        NULL,
  deleted_at        DATETIME(6)   NULL,
  deleted_by        BIGINT        NULL,
  alive             TINYINT(1)    NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY uq_lessons_course_slug (course_id, slug, alive),
  KEY ix_lessons_chapter_order (chapter_id, sort_order),
  FULLTEXT KEY ft_lessons_search (title, summary),
  CONSTRAINT fk_lessons_course     FOREIGN KEY (course_id)  REFERENCES courses (id)  ON DELETE CASCADE,
  CONSTRAINT fk_lessons_chapter    FOREIGN KEY (chapter_id) REFERENCES chapters (id) ON DELETE CASCADE,
  CONSTRAINT fk_lessons_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_lessons_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_lessons_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_lessons_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- A runnable code sample, shown in an "example" block with Try it Yourself.
CREATE TABLE code_examples (
  id           BIGINT        NOT NULL AUTO_INCREMENT,
  title        VARCHAR(200)  NOT NULL DEFAULT '',
  language     ENUM('html', 'css', 'javascript', 'python', 'sql') NOT NULL,
  starter_code MEDIUMTEXT    NOT NULL,
  run_mode     ENUM('iframe', 'pyodide', 'sqljs') NOT NULL COMMENT 'which in-browser runner',
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
  CONSTRAINT fk_code_examples_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_code_examples_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_code_examples_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_code_examples_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- A lesson is an ordered list of blocks (PLANNING.md 6.1).
-- content_html is the sanitised HTML the public page shows.
-- data holds type settings: video {provider, ref, start, caption},
-- callout {kind}, image {caption}, embed {url}.
-- Sprint 3 adds exercise and quiz blocks.
CREATE TABLE lesson_blocks (
  id              BIGINT        NOT NULL AUTO_INCREMENT,
  lesson_id       BIGINT        NOT NULL,
  type            ENUM('markdown', 'example', 'video', 'callout', 'image', 'embed') NOT NULL,
  sort_order      INT           NOT NULL DEFAULT 0,
  content_md      LONGTEXT      NULL,
  content_html    LONGTEXT      NULL,
  data            JSON          NULL,
  code_example_id BIGINT        NULL,
  media_id        BIGINT        NULL,
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
  KEY ix_lesson_blocks_lesson_order (lesson_id, sort_order),
  FULLTEXT KEY ft_lesson_blocks_search (content_md),
  CONSTRAINT fk_lesson_blocks_lesson     FOREIGN KEY (lesson_id)       REFERENCES lessons (id)       ON DELETE CASCADE,
  CONSTRAINT fk_lesson_blocks_example    FOREIGN KEY (code_example_id) REFERENCES code_examples (id) ON DELETE SET NULL,
  CONSTRAINT fk_lesson_blocks_media      FOREIGN KEY (media_id)        REFERENCES media_files (id)   ON DELETE SET NULL,
  CONSTRAINT fk_lesson_blocks_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_lesson_blocks_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_lesson_blocks_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_lesson_blocks_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE learning_paths (
  id          BIGINT        NOT NULL AUTO_INCREMENT,
  title       VARCHAR(200)  NOT NULL,
  slug        VARCHAR(100)  NOT NULL,
  description VARCHAR(1000) NOT NULL DEFAULT '',
  level       ENUM('beginner', 'intermediate', 'advanced') NOT NULL DEFAULT 'beginner',
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
  UNIQUE KEY uq_learning_paths_slug (slug, alive),
  CONSTRAINT fk_learning_paths_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_learning_paths_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_learning_paths_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_learning_paths_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Which courses a path contains, in order. Rows are replaced, not edited.
CREATE TABLE learning_path_courses (
  id         BIGINT NOT NULL AUTO_INCREMENT,
  path_id    BIGINT NOT NULL,
  course_id  BIGINT NOT NULL,
  sort_order INT    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_learning_path_courses (path_id, course_id),
  CONSTRAINT fk_learning_path_courses_path   FOREIGN KEY (path_id)   REFERENCES learning_paths (id) ON DELETE CASCADE,
  CONSTRAINT fk_learning_path_courses_course FOREIGN KEY (course_id) REFERENCES courses (id)        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
