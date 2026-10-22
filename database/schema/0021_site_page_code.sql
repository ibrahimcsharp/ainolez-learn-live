-- =====================================================================
-- 0021  website module : custom code pages
--
-- A page is either written in Markdown (as before) or made of the
-- admin's own HTML, CSS and JavaScript ('code'). A code page is served
-- by the API as its own document and shown in a sandboxed iframe, so
-- its scripts never run on the website's origin.
-- content_html of a code page keeps a sanitised copy of its HTML for
-- search engines and link previews.
-- =====================================================================

ALTER TABLE site_pages
  ADD COLUMN kind      ENUM('markdown','code') NOT NULL DEFAULT 'markdown' COMMENT 'markdown = written page, code = own HTML, CSS and JS' AFTER summary,
  ADD COLUMN code_html LONGTEXT NULL COMMENT 'code page: HTML (a fragment or a whole document)' AFTER content_html,
  ADD COLUMN code_css  LONGTEXT NULL COMMENT 'code page: CSS' AFTER code_html,
  ADD COLUMN code_js   LONGTEXT NULL COMMENT 'code page: JavaScript' AFTER code_css
