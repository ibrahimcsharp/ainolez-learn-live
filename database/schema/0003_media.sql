-- =====================================================================
-- 0003  media module : media_files (the media library)
-- The file itself lives on disk under MEDIA_ROOT; this row describes it.
-- =====================================================================

CREATE TABLE media_files (
  id            BIGINT        NOT NULL AUTO_INCREMENT,
  file_path     VARCHAR(255)  NOT NULL COMMENT 'relative to MEDIA_ROOT, e.g. uploads/2026/10/ab12.png',
  original_name VARCHAR(255)  NOT NULL,
  mime_type     VARCHAR(100)  NOT NULL,
  size_bytes    BIGINT        NOT NULL,
  width         INT           NULL COMMENT 'images only',
  height        INT           NULL,
  alt_text      VARCHAR(255)  NOT NULL DEFAULT '',
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
  UNIQUE KEY uq_media_files_path (file_path),
  KEY ix_media_files_created_by (created_by),
  CONSTRAINT fk_media_files_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_media_files_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_media_files_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_media_files_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
