-- =====================================================================
-- 0001  identity module : roles, users, auth_tokens
-- Engine InnoDB, utf8mb4_unicode_ci. Works on MySQL 8 and MariaDB 10.4+.
--
-- Record controls (on every manageable table):
--   is_active   1 = visible, 0 = hidden from public/learners
--   deleted_at  set when soft deleted (item sits in Trash)
--   alive       1 = live, NULL = soft deleted. UNIQUE(x, alive) lets a
--               deleted row's email/slug be reused, because UNIQUE
--               indexes allow many NULLs.
-- =====================================================================

CREATE TABLE roles (
  id          BIGINT       NOT NULL AUTO_INCREMENT,
  name        VARCHAR(30)  NOT NULL,
  description VARCHAR(255) NOT NULL DEFAULT '',
  created_at  DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY uq_roles_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO roles (name, description) VALUES
  ('super_admin', 'Full control of the platform'),
  ('learner',     'Registered learner');


CREATE TABLE users (
  id                BIGINT        NOT NULL AUTO_INCREMENT,
  role_id           BIGINT        NOT NULL,
  email             VARCHAR(191)  NOT NULL,
  username          VARCHAR(50)   NOT NULL,
  password          VARCHAR(128)  NOT NULL COMMENT 'Django password hash',
  full_name         VARCHAR(120)  NOT NULL DEFAULT '',
  headline          VARCHAR(160)  NOT NULL DEFAULT '',
  bio               VARCHAR(1000) NOT NULL DEFAULT '',
  country           CHAR(2)       NOT NULL DEFAULT '' COMMENT 'ISO 3166-1 alpha-2',
  avatar_url        VARCHAR(500)  NOT NULL DEFAULT '',
  is_email_verified TINYINT(1)    NOT NULL DEFAULT 0,
  is_banned         TINYINT(1)    NOT NULL DEFAULT 0,
  ban_reason        VARCHAR(255)  NOT NULL DEFAULT '',
  last_login_at     DATETIME(6)   NULL,
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
  UNIQUE KEY uq_users_email    (email, alive),
  UNIQUE KEY uq_users_username (username, alive),
  KEY ix_users_role (role_id),
  CONSTRAINT fk_users_role       FOREIGN KEY (role_id)    REFERENCES roles (id) ON DELETE RESTRICT,
  CONSTRAINT fk_users_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_users_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_users_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_users_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- One-time tokens for email verification and password reset.
-- Only the SHA-256 hash is stored; the raw token lives in the emailed link.
CREATE TABLE auth_tokens (
  id         BIGINT      NOT NULL AUTO_INCREMENT,
  user_id    BIGINT      NOT NULL,
  type       ENUM('verify_email', 'reset_password') NOT NULL,
  token_hash CHAR(64)    NOT NULL,
  expires_at DATETIME(6) NOT NULL,
  used_at    DATETIME(6) NULL,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY uq_auth_tokens_hash (token_hash),
  KEY ix_auth_tokens_user_type (user_id, type),
  CONSTRAINT fk_auth_tokens_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
