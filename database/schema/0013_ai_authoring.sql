-- =====================================================================
-- 0013  ai_authoring module (AI course generator, PLANNING.md 6.7)
--       ai_course_jobs, plus an ai_generated flag on courses and lessons
--
-- Flow: the admin describes a course -> Claude proposes an outline ->
-- the admin edits it -> Claude drafts every lesson (one job each) ->
-- everything stays a draft until the admin reviews and publishes it.
-- =====================================================================

ALTER TABLE courses ADD COLUMN ai_generated TINYINT(1) NOT NULL DEFAULT 0 AFTER status;
ALTER TABLE lessons ADD COLUMN ai_generated TINYINT(1) NOT NULL DEFAULT 0 AFTER status;


CREATE TABLE ai_course_jobs (
  id                  BIGINT        NOT NULL AUTO_INCREMENT,
  topic               VARCHAR(200)  NOT NULL,
  level               ENUM('beginner', 'intermediate', 'advanced') NOT NULL DEFAULT 'beginner',
  audience            VARCHAR(300)  NOT NULL DEFAULT '',
  language_key        ENUM('html', 'css', 'javascript', 'python', 'sql', 'ai', 'other') NOT NULL DEFAULT 'python',
  category_id         BIGINT        NULL,
  chapters_count      TINYINT       NOT NULL DEFAULT 5,
  lessons_per_chapter TINYINT       NOT NULL DEFAULT 4,
  notes               TEXT          NULL COMMENT 'extra instructions from the admin',
  outline             JSON          NULL COMMENT '{title, short_description, description, chapters: [{title, description, lessons: [{title, summary, lesson_id}]}]}',
  status              ENUM('outline_queued', 'outline_ready', 'generating', 'drafted', 'failed') NOT NULL DEFAULT 'outline_queued',
  course_id           BIGINT        NULL COMMENT 'the draft course, once generating starts',
  lessons_total       INT           NOT NULL DEFAULT 0,
  lessons_done        INT           NOT NULL DEFAULT 0,
  lessons_failed      INT           NOT NULL DEFAULT 0,
  tokens_in           BIGINT        NOT NULL DEFAULT 0,
  tokens_out          BIGINT        NOT NULL DEFAULT 0,
  cost_usd            DECIMAL(10,4) NOT NULL DEFAULT 0,
  error               VARCHAR(1000) NOT NULL DEFAULT '',
  -- record controls
  is_active           TINYINT(1)    NOT NULL DEFAULT 1,
  created_at          DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at          DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by          BIGINT        NULL,
  updated_by          BIGINT        NULL,
  deleted_at          DATETIME(6)   NULL,
  deleted_by          BIGINT        NULL,
  alive               TINYINT(1)    NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY ix_ai_course_jobs_status (status),
  CONSTRAINT fk_ai_course_jobs_category   FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
  CONSTRAINT fk_ai_course_jobs_course     FOREIGN KEY (course_id)   REFERENCES courses (id)    ON DELETE SET NULL,
  CONSTRAINT fk_ai_course_jobs_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_ai_course_jobs_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_ai_course_jobs_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_ai_course_jobs_counts CHECK (chapters_count BETWEEN 1 AND 15 AND lessons_per_chapter BETWEEN 1 AND 10),
  CONSTRAINT ck_ai_course_jobs_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
