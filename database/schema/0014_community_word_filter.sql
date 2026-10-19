-- =====================================================================
-- 0014  community : blocked words
--
-- community_settings (one row) holds the words and phrases the admin does
-- not want in posts, replies and lesson comments, edited in
-- Admin -> Community -> Blocked words.
--   hold    the text is saved but waits in the moderation queue, even for
--           trusted members (the queue shows which words matched)
--   refuse  the text is not saved; the writer is asked to change it
-- Matching ignores case and only matches whole words, so "class" does not
-- match a blocked "ass".
-- =====================================================================

CREATE TABLE community_settings (
  id             TINYINT                  NOT NULL DEFAULT 1,
  blocked_words  TEXT                     NULL COMMENT 'one word or phrase per line',
  blocked_action ENUM('hold', 'refuse')   NOT NULL DEFAULT 'hold',
  updated_at     DATETIME(6)              NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  updated_by     BIGINT                   NULL,
  PRIMARY KEY (id),
  CONSTRAINT ck_community_settings_single CHECK (id = 1),
  CONSTRAINT fk_community_settings_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO community_settings (id, blocked_words) VALUES (1, '');
