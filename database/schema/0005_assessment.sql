-- =====================================================================
-- 0005  assessment module : exercises, quizzes, quiz_questions, quiz_options
-- Also lets lesson blocks show an exercise or a quiz.
-- Code runs in the learner's browser; the server only checks the result.
-- =====================================================================

CREATE TABLE exercises (
  id             BIGINT        NOT NULL AUTO_INCREMENT,
  title          VARCHAR(200)  NOT NULL DEFAULT '',
  prompt_md      TEXT          NOT NULL,
  prompt_html    TEXT          NOT NULL COMMENT 'sanitised HTML of prompt_md',
  language       ENUM('html', 'css', 'javascript', 'python', 'sql') NOT NULL,
  starter_code   MEDIUMTEXT    NOT NULL,
  solution_code  MEDIUMTEXT    NOT NULL,
  check_type     ENUM('exact', 'contains', 'regex', 'output') NOT NULL DEFAULT 'output'
                 COMMENT 'exact/contains/regex test the code, output tests what it printed',
  expected_value TEXT          NOT NULL,
  hint           VARCHAR(500)  NOT NULL DEFAULT '',
  -- record controls
  is_active      TINYINT(1)    NOT NULL DEFAULT 1,
  created_at     DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at     DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by     BIGINT        NULL,
  updated_by     BIGINT        NULL,
  deleted_at     DATETIME(6)   NULL,
  deleted_by     BIGINT        NULL,
  alive          TINYINT(1)    NULL DEFAULT 1,
  PRIMARY KEY (id),
  CONSTRAINT fk_exercises_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_exercises_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_exercises_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_exercises_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- A final quiz (is_final = 1) must be passed to complete its course.
CREATE TABLE quizzes (
  id              BIGINT        NOT NULL AUTO_INCREMENT,
  course_id       BIGINT        NOT NULL,
  title           VARCHAR(200)  NOT NULL,
  description     VARCHAR(500)  NOT NULL DEFAULT '',
  is_final        TINYINT(1)    NOT NULL DEFAULT 0,
  pass_percentage TINYINT UNSIGNED NOT NULL DEFAULT 70,
  max_attempts    INT           NULL COMMENT 'NULL = unlimited',
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
  KEY ix_quizzes_course (course_id),
  CONSTRAINT fk_quizzes_course     FOREIGN KEY (course_id)  REFERENCES courses (id) ON DELETE CASCADE,
  CONSTRAINT fk_quizzes_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_quizzes_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_quizzes_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_quizzes_pass CHECK (pass_percentage BETWEEN 1 AND 100),
  CONSTRAINT ck_quizzes_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE quiz_questions (
  id            BIGINT        NOT NULL AUTO_INCREMENT,
  quiz_id       BIGINT        NOT NULL,
  question_text TEXT          NOT NULL,
  question_type ENUM('single', 'multiple', 'true_false') NOT NULL DEFAULT 'single',
  code_snippet  TEXT          NULL COMMENT 'optional code shown with the question',
  explanation   VARCHAR(1000) NOT NULL DEFAULT '' COMMENT 'shown after answering',
  points        INT           NOT NULL DEFAULT 1,
  sort_order    INT           NOT NULL DEFAULT 0,
  -- record controls
  is_active     TINYINT(1)    NOT NULL DEFAULT 1,
  created_at    DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at    DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by    BIGINT        NULL,
  updated_by    BIGINT        NULL,
  deleted_at    DATETIME(6)   NULL,
  deleted_by    BIGINT        NULL,
  alive         TINYINT(1)    NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY ix_quiz_questions_quiz_order (quiz_id, sort_order),
  CONSTRAINT fk_quiz_questions_quiz       FOREIGN KEY (quiz_id)    REFERENCES quizzes (id) ON DELETE CASCADE,
  CONSTRAINT fk_quiz_questions_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_quiz_questions_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_quiz_questions_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_quiz_questions_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Options are edited together with their question, so they are plain rows.
CREATE TABLE quiz_options (
  id          BIGINT        NOT NULL AUTO_INCREMENT,
  question_id BIGINT        NOT NULL,
  option_text VARCHAR(500)  NOT NULL,
  is_correct  TINYINT(1)    NOT NULL DEFAULT 0,
  sort_order  INT           NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY ix_quiz_options_question (question_id, sort_order),
  CONSTRAINT fk_quiz_options_question FOREIGN KEY (question_id) REFERENCES quiz_questions (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE lesson_blocks
  MODIFY type ENUM('markdown', 'example', 'video', 'callout', 'image', 'embed', 'exercise', 'quiz') NOT NULL,
  ADD COLUMN exercise_id BIGINT NULL AFTER code_example_id,
  ADD COLUMN quiz_id     BIGINT NULL AFTER exercise_id,
  ADD CONSTRAINT fk_lesson_blocks_exercise FOREIGN KEY (exercise_id) REFERENCES exercises (id) ON DELETE SET NULL,
  ADD CONSTRAINT fk_lesson_blocks_quiz     FOREIGN KEY (quiz_id)     REFERENCES quizzes (id)   ON DELETE SET NULL;
