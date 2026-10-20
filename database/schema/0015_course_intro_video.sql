-- =====================================================================
-- 0015  catalog : an optional intro video at the top of a course page.
--       Any link the lesson video block accepts (YouTube, Vimeo, Loom,
--       Google Drive or an .mp4 file), stored as the admin typed it.
-- =====================================================================

ALTER TABLE courses
  ADD COLUMN intro_video_url VARCHAR(500) NOT NULL DEFAULT '' AFTER thumbnail_media_id;
