-- =====================================================================
-- 0008  certification module : certificate_templates, certificates
-- A certificate keeps a copy of the learner's name and the course title
-- as they were on the day it was issued.
-- =====================================================================

CREATE TABLE certificate_templates (
  id            BIGINT        NOT NULL AUTO_INCREMENT,
  name          VARCHAR(100)  NOT NULL,
  heading       VARCHAR(100)  NOT NULL DEFAULT 'Certificate of Completion',
  body_text     VARCHAR(300)  NOT NULL DEFAULT 'has successfully completed the course',
  signer_name   VARCHAR(100)  NOT NULL DEFAULT '',
  signer_title  VARCHAR(100)  NOT NULL DEFAULT '',
  primary_color CHAR(7)       NOT NULL DEFAULT '#05192D',
  accent_color  CHAR(7)       NOT NULL DEFAULT '#03EF62',
  is_default    TINYINT(1)    NOT NULL DEFAULT 0,
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
  CONSTRAINT fk_certificate_templates_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_certificate_templates_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_certificate_templates_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_certificate_templates_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO certificate_templates (name, signer_name, signer_title, is_default)
  VALUES ('ainolez classic', 'The ainolez team', 'Learn it. Code it. Own it.', 1);


CREATE TABLE certificates (
  id             BIGINT        NOT NULL AUTO_INCREMENT,
  user_id        BIGINT        NOT NULL,
  course_id      BIGINT        NOT NULL,
  template_id    BIGINT        NULL,
  certificate_code CHAR(12)    NOT NULL COMMENT 'public id in the verify URL',
  status         ENUM('pending_review', 'issued', 'revoked') NOT NULL DEFAULT 'issued',
  learner_name   VARCHAR(120)  NOT NULL,
  course_title   VARCHAR(200)  NOT NULL,
  pdf_path       VARCHAR(255)  NOT NULL DEFAULT '' COMMENT 'relative to MEDIA_ROOT, set by the render job',
  image_path     VARCHAR(255)  NOT NULL DEFAULT '' COMMENT '1200x627 share image',
  issued_at      DATETIME(6)   NULL,
  revoked_at     DATETIME(6)   NULL,
  revoke_reason  VARCHAR(255)  NOT NULL DEFAULT '',
  view_count     INT           NOT NULL DEFAULT 0,
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
  UNIQUE KEY uq_certificates_code (certificate_code),
  UNIQUE KEY uq_certificates_user_course (user_id, course_id, alive),
  KEY ix_certificates_status (status),
  CONSTRAINT fk_certificates_user       FOREIGN KEY (user_id)     REFERENCES users (id)                 ON DELETE CASCADE,
  CONSTRAINT fk_certificates_course     FOREIGN KEY (course_id)   REFERENCES courses (id)               ON DELETE RESTRICT,
  CONSTRAINT fk_certificates_template   FOREIGN KEY (template_id) REFERENCES certificate_templates (id) ON DELETE SET NULL,
  CONSTRAINT fk_certificates_created_by FOREIGN KEY (created_by)  REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_certificates_updated_by FOREIGN KEY (updated_by)  REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_certificates_deleted_by FOREIGN KEY (deleted_by)  REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_certificates_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
