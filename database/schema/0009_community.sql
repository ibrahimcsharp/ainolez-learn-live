-- =====================================================================
-- 0009  community module : community_spaces, community_posts,
--       community_replies, lesson_comments, reactions, content_reports
-- Posts, replies and comments start as 'pending' unless the space is open
-- and the author is trusted (enough points); a moderator approves them.
-- =====================================================================

CREATE TABLE community_spaces (
  id           BIGINT       NOT NULL AUTO_INCREMENT,
  name         VARCHAR(100) NOT NULL,
  slug         VARCHAR(100) NOT NULL,
  description  VARCHAR(500) NOT NULL DEFAULT '',
  icon         VARCHAR(50)  NOT NULL DEFAULT '💬',
  sort_order   INT          NOT NULL DEFAULT 0,
  posting_rule ENUM('open', 'approval_required') NOT NULL DEFAULT 'open'
               COMMENT 'open = trusted members post straight away',
  -- record controls
  is_active    TINYINT(1)   NOT NULL DEFAULT 1,
  created_at   DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at   DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by   BIGINT       NULL,
  updated_by   BIGINT       NULL,
  deleted_at   DATETIME(6)  NULL,
  deleted_by   BIGINT       NULL,
  alive        TINYINT(1)   NULL DEFAULT 1,
  PRIMARY KEY (id),
  UNIQUE KEY uq_community_spaces_slug (slug, alive),
  CONSTRAINT fk_community_spaces_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_community_spaces_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_community_spaces_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_community_spaces_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO community_spaces (name, slug, description, icon, sort_order) VALUES
  ('General',           'general',      'Say hello and talk about learning.', '👋', 1),
  ('HTML & CSS',        'html-css',     'Web pages and styling.',             '🎨', 2),
  ('JavaScript',        'javascript',   'Scripts, the DOM and the browser.',  '⚡', 3),
  ('Python',            'python',       'Python questions and tips.',         '🐍', 4),
  ('AI & ML',           'ai-ml',        'Machine learning and AI tools.',     '🤖', 5),
  ('Show your project', 'show-project', 'Share what you built.',              '🚀', 6),
  ('Help',              'help',         'Stuck? Ask here.',                   '🆘', 7);


CREATE TABLE community_posts (
  id             BIGINT       NOT NULL AUTO_INCREMENT,
  space_id       BIGINT       NOT NULL,
  user_id        BIGINT       NOT NULL,
  title          VARCHAR(200) NOT NULL,
  body_md        TEXT         NOT NULL,
  body_html      TEXT         NOT NULL COMMENT 'sanitised HTML of body_md',
  status         ENUM('pending', 'approved', 'rejected', 'hidden') NOT NULL DEFAULT 'pending',
  reject_reason  VARCHAR(255) NOT NULL DEFAULT '',
  is_pinned      TINYINT(1)   NOT NULL DEFAULT 0,
  is_locked      TINYINT(1)   NOT NULL DEFAULT 0 COMMENT 'locked = no new replies',
  reply_count    INT          NOT NULL DEFAULT 0 COMMENT 'approved replies',
  reaction_count INT          NOT NULL DEFAULT 0,
  -- record controls
  is_active      TINYINT(1)   NOT NULL DEFAULT 1,
  created_at     DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at     DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by     BIGINT       NULL,
  updated_by     BIGINT       NULL,
  deleted_at     DATETIME(6)  NULL,
  deleted_by     BIGINT       NULL,
  alive          TINYINT(1)   NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY ix_community_posts_space_status (space_id, status, is_pinned),
  KEY ix_community_posts_user (user_id),
  FULLTEXT KEY ft_community_posts_search (title, body_md),
  CONSTRAINT fk_community_posts_space      FOREIGN KEY (space_id)   REFERENCES community_spaces (id) ON DELETE CASCADE,
  CONSTRAINT fk_community_posts_user       FOREIGN KEY (user_id)    REFERENCES users (id)            ON DELETE CASCADE,
  CONSTRAINT fk_community_posts_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_community_posts_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_community_posts_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_community_posts_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE community_replies (
  id             BIGINT       NOT NULL AUTO_INCREMENT,
  post_id        BIGINT       NOT NULL,
  user_id        BIGINT       NOT NULL,
  body_md        TEXT         NOT NULL,
  body_html      TEXT         NOT NULL,
  status         ENUM('pending', 'approved', 'rejected', 'hidden') NOT NULL DEFAULT 'pending',
  reject_reason  VARCHAR(255) NOT NULL DEFAULT '',
  is_helpful     TINYINT(1)   NOT NULL DEFAULT 0 COMMENT 'accepted by the post author',
  reaction_count INT          NOT NULL DEFAULT 0,
  -- record controls
  is_active      TINYINT(1)   NOT NULL DEFAULT 1,
  created_at     DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at     DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by     BIGINT       NULL,
  updated_by     BIGINT       NULL,
  deleted_at     DATETIME(6)  NULL,
  deleted_by     BIGINT       NULL,
  alive          TINYINT(1)   NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY ix_community_replies_post_status (post_id, status),
  CONSTRAINT fk_community_replies_post       FOREIGN KEY (post_id)    REFERENCES community_posts (id) ON DELETE CASCADE,
  CONSTRAINT fk_community_replies_user       FOREIGN KEY (user_id)    REFERENCES users (id)           ON DELETE CASCADE,
  CONSTRAINT fk_community_replies_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_community_replies_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_community_replies_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_community_replies_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE lesson_comments (
  id             BIGINT       NOT NULL AUTO_INCREMENT,
  lesson_id      BIGINT       NOT NULL,
  user_id        BIGINT       NOT NULL,
  body_md        TEXT         NOT NULL,
  body_html      TEXT         NOT NULL,
  status         ENUM('pending', 'approved', 'rejected', 'hidden') NOT NULL DEFAULT 'pending',
  reject_reason  VARCHAR(255) NOT NULL DEFAULT '',
  reaction_count INT          NOT NULL DEFAULT 0,
  -- record controls
  is_active      TINYINT(1)   NOT NULL DEFAULT 1,
  created_at     DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at     DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  created_by     BIGINT       NULL,
  updated_by     BIGINT       NULL,
  deleted_at     DATETIME(6)  NULL,
  deleted_by     BIGINT       NULL,
  alive          TINYINT(1)   NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY ix_lesson_comments_lesson_status (lesson_id, status),
  CONSTRAINT fk_lesson_comments_lesson     FOREIGN KEY (lesson_id)  REFERENCES lessons (id) ON DELETE CASCADE,
  CONSTRAINT fk_lesson_comments_user       FOREIGN KEY (user_id)    REFERENCES users (id)   ON DELETE CASCADE,
  CONSTRAINT fk_lesson_comments_created_by FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_lesson_comments_updated_by FOREIGN KEY (updated_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT fk_lesson_comments_deleted_by FOREIGN KEY (deleted_by) REFERENCES users (id) ON DELETE SET NULL,
  CONSTRAINT ck_lesson_comments_alive CHECK (
    (deleted_at IS NULL AND alive = 1) OR (deleted_at IS NOT NULL AND alive IS NULL)
  )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- One like per person per item.
CREATE TABLE reactions (
  id          BIGINT       NOT NULL AUTO_INCREMENT,
  user_id     BIGINT       NOT NULL,
  target_type ENUM('post', 'reply', 'comment') NOT NULL,
  target_id   BIGINT       NOT NULL,
  type        ENUM('like') NOT NULL DEFAULT 'like',
  created_at  DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY uq_reactions_once (user_id, target_type, target_id, type),
  KEY ix_reactions_target (target_type, target_id),
  CONSTRAINT fk_reactions_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE content_reports (
  id              BIGINT       NOT NULL AUTO_INCREMENT,
  reporter_id     BIGINT       NOT NULL,
  target_type     ENUM('post', 'reply', 'comment') NOT NULL,
  target_id       BIGINT       NOT NULL,
  reason          VARCHAR(500) NOT NULL,
  status          ENUM('open', 'resolved', 'dismissed') NOT NULL DEFAULT 'open',
  resolved_by     BIGINT       NULL,
  resolution_note VARCHAR(500) NOT NULL DEFAULT '',
  created_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  resolved_at     DATETIME(6)  NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_content_reports_once (reporter_id, target_type, target_id),
  KEY ix_content_reports_status (status),
  CONSTRAINT fk_content_reports_reporter FOREIGN KEY (reporter_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_content_reports_resolver FOREIGN KEY (resolved_by) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Community rewards (PLANNING.md 6.4)
INSERT INTO points_rules (event_key, points, description) VALUES
  ('first_post',     10, 'First approved community post'),
  ('helpful_answer', 20, 'Answer marked helpful by the asker');
