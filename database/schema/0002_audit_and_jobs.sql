-- =====================================================================
-- 0002  shared kernel : audit_logs, jobs
-- Both are append/process tables, so they have no record controls.
-- =====================================================================

-- Who did what, and when. Never edited; purged by a retention job later.
CREATE TABLE audit_logs (
  id          BIGINT      NOT NULL AUTO_INCREMENT,
  user_id     BIGINT      NULL COMMENT 'NULL = system or anonymous',
  action      VARCHAR(60) NOT NULL COMMENT 'e.g. user.registered, course.published',
  entity_type VARCHAR(60) NOT NULL DEFAULT '',
  entity_id   BIGINT      NULL,
  before_data JSON        NULL,
  after_data  JSON        NULL,
  ip_address  VARCHAR(45) NOT NULL DEFAULT '',
  created_at  DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  KEY ix_audit_logs_entity  (entity_type, entity_id),
  KEY ix_audit_logs_user    (user_id),
  KEY ix_audit_logs_created (created_at),
  CONSTRAINT fk_audit_logs_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Background job queue. cPanel has no Redis/Celery, so cron runs
-- "manage.py run_jobs" every minute and works through this table.
CREATE TABLE jobs (
  id          BIGINT           NOT NULL AUTO_INCREMENT,
  type        VARCHAR(100)     NOT NULL COMMENT 'registered handler name',
  payload     JSON             NOT NULL,
  status      ENUM('queued', 'running', 'done', 'failed') NOT NULL DEFAULT 'queued',
  attempts    TINYINT UNSIGNED NOT NULL DEFAULT 0,
  run_after   DATETIME(6)      NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  last_error  VARCHAR(2000)    NOT NULL DEFAULT '',
  created_at  DATETIME(6)      NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  started_at  DATETIME(6)      NULL,
  finished_at DATETIME(6)      NULL,
  PRIMARY KEY (id),
  KEY ix_jobs_status_run_after (status, run_after)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
