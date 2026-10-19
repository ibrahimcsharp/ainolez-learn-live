-- =====================================================================
-- 0007  gamification module : points_rules, points_ledger, learner_stats,
--       badges, user_badges  (+ leaderboard opt-out on users)
-- Points are only ever added to the append-only ledger; learner_stats
-- caches the totals. UNIQUE(user, event, ref) stops double awards.
-- =====================================================================

CREATE TABLE points_rules (
  id          BIGINT       NOT NULL AUTO_INCREMENT,
  event_key   VARCHAR(50)  NOT NULL,
  points      INT          NOT NULL,
  daily_cap   INT          NULL COMMENT 'max points per day from this rule, NULL = no cap',
  description VARCHAR(255) NOT NULL DEFAULT '',
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
  UNIQUE KEY uq_points_rules_event (event_key, alive),
  CONSTRAINT fk_points_rules_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_points_rules_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_points_rules_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_points_rules_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO points_rules (event_key, points, description) VALUES
  ('lesson_completed',  10,  'Finish a lesson'),
  ('exercise_solved',   15,  'Solve an exercise (first time)'),
  ('quiz_passed',       50,  'Pass a quiz'),
  ('quiz_perfect',      20,  'Bonus for 100% in a quiz'),
  ('course_completed',  200, 'Finish a whole course'),
  ('streak_day',        5,   'Learn on another day in a row');


CREATE TABLE points_ledger (
  id         BIGINT      NOT NULL AUTO_INCREMENT,
  user_id    BIGINT      NOT NULL,
  rule_id    BIGINT      NULL,
  event_key  VARCHAR(50) NOT NULL,
  points     INT         NOT NULL,
  ref_type   VARCHAR(30) NOT NULL COMMENT 'what earned it: lesson, exercise, quiz, course, day',
  ref_id     BIGINT      NOT NULL,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY uq_points_ledger_once (user_id, event_key, ref_type, ref_id),
  KEY ix_points_ledger_created (created_at),
  CONSTRAINT fk_points_ledger_user FOREIGN KEY (user_id) REFERENCES users (id)        ON DELETE CASCADE,
  CONSTRAINT fk_points_ledger_rule FOREIGN KEY (rule_id) REFERENCES points_rules (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE learner_stats (
  user_id           BIGINT      NOT NULL,
  total_points      INT         NOT NULL DEFAULT 0,
  current_streak    INT         NOT NULL DEFAULT 0 COMMENT 'days in a row with learning activity',
  longest_streak    INT         NOT NULL DEFAULT 0,
  last_active_date  DATE        NULL,
  lessons_completed INT         NOT NULL DEFAULT 0,
  courses_completed INT         NOT NULL DEFAULT 0,
  updated_at        DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (user_id),
  KEY ix_learner_stats_points (total_points),
  CONSTRAINT fk_learner_stats_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- rule: {"type": "points" | "lessons" | "courses" | "streak", "threshold": 7}
CREATE TABLE badges (
  id          BIGINT       NOT NULL AUTO_INCREMENT,
  name        VARCHAR(100) NOT NULL,
  slug        VARCHAR(100) NOT NULL,
  description VARCHAR(255) NOT NULL DEFAULT '',
  icon        VARCHAR(50)  NOT NULL DEFAULT '🏅' COMMENT 'emoji',
  rule        JSON         NOT NULL,
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
  UNIQUE KEY uq_badges_slug (slug, alive),
  CONSTRAINT fk_badges_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_badges_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_badges_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_badges_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO badges (name, slug, description, icon, rule) VALUES
  ('First steps',     'first-steps',     'Finish your first lesson',  '👣', '{"type": "lessons", "threshold": 1}'),
  ('On fire',         'on-fire',         'Learn 7 days in a row',     '🔥', '{"type": "streak", "threshold": 7}'),
  ('Course finisher', 'course-finisher', 'Finish your first course',  '🎓', '{"type": "courses", "threshold": 1}'),
  ('Point collector', 'point-collector', 'Earn 500 points',           '💎', '{"type": "points", "threshold": 500}');


CREATE TABLE user_badges (
  id         BIGINT      NOT NULL AUTO_INCREMENT,
  user_id    BIGINT      NOT NULL,
  badge_id   BIGINT      NOT NULL,
  awarded_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY uq_user_badges (user_id, badge_id),
  CONSTRAINT fk_user_badges_user  FOREIGN KEY (user_id)  REFERENCES users (id)  ON DELETE CASCADE,
  CONSTRAINT fk_user_badges_badge FOREIGN KEY (badge_id) REFERENCES badges (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE users
  ADD COLUMN show_on_leaderboard TINYINT(1) NOT NULL DEFAULT 1 AFTER ban_reason;
