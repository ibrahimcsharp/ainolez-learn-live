-- =====================================================================
-- 0016  assistant : switch the AI course generator on or off, next to
--       the tutor's own switch (ai_settings.enabled).
-- =====================================================================

ALTER TABLE ai_settings
  ADD COLUMN course_generator_enabled TINYINT(1) NOT NULL DEFAULT 1 AFTER enabled_for_learners;
