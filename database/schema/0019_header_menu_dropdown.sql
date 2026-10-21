-- =====================================================================
-- 0019  website module : a header menu can be its own dropdown
--
--   menus.show_as   header only: 'dropdown' shows the menu's name in the
--                   bar with its links under it, 'links' puts its links
--                   side by side in the bar. Footer menus are columns.
-- The seeded Main menu keeps its links in the bar.
-- =====================================================================

ALTER TABLE menus
  ADD COLUMN show_as ENUM('links', 'dropdown') NOT NULL DEFAULT 'dropdown'
    COMMENT 'header: a dropdown named after the menu, or its links in the bar' AFTER location;

UPDATE menus SET show_as = 'links' WHERE id = 1;
