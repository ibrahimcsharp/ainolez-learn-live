-- =====================================================================
-- 0018  website module : sub-menus
--
--   menu_items.parent_id   a link can sit under another link of the same
--                          menu (one level): a dropdown in the header, an
--                          indented list in a footer column
--   link_type 'none'       a top-level heading with no link of its own,
--                          only there to hold its sub-menu
-- Deleting a link for real removes its sub-menu links too.
-- =====================================================================

ALTER TABLE menu_items
  ADD COLUMN parent_id BIGINT NULL COMMENT 'the link this one sits under' AFTER menu_id,
  ADD KEY ix_menu_items_parent_order (parent_id, sort_order),
  ADD CONSTRAINT fk_menu_items_parent FOREIGN KEY (parent_id) REFERENCES menu_items (id) ON DELETE CASCADE,
  MODIFY link_type ENUM('page', 'course', 'url', 'none') NOT NULL;

ALTER TABLE menu_items DROP CONSTRAINT ck_menu_items_target;

ALTER TABLE menu_items
  ADD CONSTRAINT ck_menu_items_target CHECK (
    (link_type = 'page' AND page_id IS NOT NULL AND course_id IS NULL)
    OR (link_type = 'course' AND course_id IS NOT NULL AND page_id IS NULL)
    OR (link_type = 'url' AND url <> '' AND page_id IS NULL AND course_id IS NULL)
    OR (link_type = 'none' AND label <> '' AND parent_id IS NULL
        AND page_id IS NULL AND course_id IS NULL AND url = '')
  );
