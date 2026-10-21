-- =====================================================================
-- 0020  website module : one order for the whole header bar
--
-- The header bar mixes the links of "links" header menus and whole
-- "dropdown" header menus. header_position orders them all together, so
-- a dropdown can sit between two links (Admin -> Menus -> Header bar).
-- NULL: not placed yet, shown after the placed ones in menu order.
-- =====================================================================

ALTER TABLE menus
  ADD COLUMN header_position INT NULL COMMENT 'place of a dropdown menu in the header bar' AFTER sort_order;

ALTER TABLE menu_items
  ADD COLUMN header_position INT NULL COMMENT 'place of a top-level link in the header bar' AFTER sort_order;
