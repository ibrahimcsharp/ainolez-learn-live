-- =====================================================================
-- 0012  seo : default share image and logo, now that the brand images
--       exist (frontend/public/brand/og-default.png, logo-512.png).
-- =====================================================================

UPDATE seo_settings
SET default_image_url     = '/brand/og-default.png',
    organization_logo_url = '/brand/logo-512.png'
WHERE id = 1 AND default_image_url = '' AND organization_logo_url = '';
