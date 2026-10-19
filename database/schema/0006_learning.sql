-- =====================================================================
-- 0006  learning module : enrollments, lesson_progress,
--       exercise_submissions, quiz_attempts
-- A learner's own records. They are history, so they have no record
-- controls; they are removed only when the user or course is removed.
-- =====================================================================

CREATE TABLE enrollments (
  id               BIGINT           NOT NULL AUTO_INCREMENT,
  user_id          BIGINT           NOT NULL,
  course_id        BIGINT           NOT NULL,
  status           ENUM('active', 'completed') NOT NULL DEFAULT 'active',
  progress_percent TINYINT UNSIGNED NOT NULL DEFAULT 0,
  last_lesson_id   BIGINT           NULL COMMENT 'where "Resume" goes',
  started_at       DATETIME(6)      NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  completed_at     DATETIME(6)      NULL,
  updated_at       DATETIME(6)      NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY uq_enrollments_user_course (user_id, course_id),
  KEY ix_enrollments_course (course_id),
  CONSTRAINT fk_enrollments_user        FOREIGN KEY (user_id)        REFERENCES users (id)   ON DELETE CASCADE,
  CONSTRAINT fk_enrollments_course      FOREIGN KEY (course_id)      REFERENCES courses (id) ON DELETE CASCADE,
  CONSTRAINT fk_enrollments_last_lesson FOREIGN KEY (last_lesson_id) REFERENCES lessons (id) ON DELETE SET NULL,
  CONSTRAINT ck_enrollments_percent CHECK (progress_percent <= 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE lesson_progress (
  id           BIGINT      NOT NULL AUTO_INCREMENT,
  user_id      BIGINT      NOT NULL,
  lesson_id    BIGINT      NOT NULL,
  course_id    BIGINT      NOT NULL COMMENT 'copied from the lesson for fast counting',
  completed_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY uq_lesson_progress_user_lesson (user_id, lesson_id),
  KEY ix_lesson_progress_user_course (user_id, course_id),
  CONSTRAINT fk_lesson_progress_user   FOREIGN KEY (user_id)   REFERENCES users (id)   ON DELETE CASCADE,
  CONSTRAINT fk_lesson_progress_lesson FOREIGN KEY (lesson_id) REFERENCES lessons (id) ON DELETE CASCADE,
  CONSTRAINT fk_lesson_progress_course FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE exercise_submissions (
  id          BIGINT      NOT NULL AUTO_INCREMENT,
  user_id     BIGINT      NOT NULL,
  exercise_id BIGINT      NOT NULL,
  code        MEDIUMTEXT  NOT NULL,
  output      TEXT        NULL COMMENT 'what the code printed in the browser',
  is_correct  TINYINT(1)  NOT NULL,
  created_at  DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  KEY ix_exercise_submissions_user_exercise (user_id, exercise_id),
  CONSTRAINT fk_exercise_submissions_user     FOREIGN KEY (user_id)     REFERENCES users (id)     ON DELETE CASCADE,
  CONSTRAINT fk_exercise_submissions_exercise FOREIGN KEY (exercise_id) REFERENCES exercises (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- answers holds {question_id: [chosen option ids]} as submitted.
CREATE TABLE quiz_attempts (
  id           BIGINT        NOT NULL AUTO_INCREMENT,
  user_id      BIGINT        NOT NULL,
  quiz_id      BIGINT        NOT NULL,
  score        INT           NOT NULL,
  total_points INT           NOT NULL,
  percentage   DECIMAL(5, 2) NOT NULL,
  passed       TINYINT(1)    NOT NULL,
  answers      JSON          NOT NULL,
  created_at   DATETIME(6)   NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  KEY ix_quiz_attempts_user_quiz (user_id, quiz_id),
  CONSTRAINT fk_quiz_attempts_user FOREIGN KEY (user_id) REFERENCES users (id)   ON DELETE CASCADE,
  CONSTRAINT fk_quiz_attempts_quiz FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
