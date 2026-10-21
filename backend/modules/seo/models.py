"""Tables from database/schema/0011_seo.sql."""

from django.conf import settings
from django.db import models

from shared.models import BaseModel


class SeoSettings(models.Model):
    """Singleton (id = 1): site-wide SEO defaults."""

    site_name = models.CharField(max_length=60, default="ainolez")
    title_template = models.CharField(max_length=100, default="{title} · ainolez")
    default_description = models.CharField(max_length=300, blank=True)
    default_keywords = models.CharField(max_length=500, blank=True)
    default_image_url = models.CharField(max_length=500, blank=True)
    locale = models.CharField(max_length=10, default="en_US")
    twitter_site = models.CharField(max_length=50, blank=True)
    facebook_app_id = models.CharField(max_length=50, blank=True)
    google_site_verification = models.CharField(max_length=100, blank=True)
    bing_site_verification = models.CharField(max_length=100, blank=True)
    organization_logo_url = models.CharField(max_length=500, blank=True)
    social_profiles = models.JSONField(default=list)
    allow_indexing = models.BooleanField(default=True)
    robots_txt_extra = models.TextField(null=True, blank=True)
    last_build_at = models.DateTimeField(null=True)
    last_build_pages = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        db_column="updated_by",
    )

    class Meta:
        managed = False
        db_table = "seo_settings"


class SeoPage(BaseModel):
    """SEO settings of one page. Empty text and NULL mean "automatic"."""

    class Entity(models.TextChoices):
        COURSE = "course"
        LESSON = "lesson"
        POST = "post"
        PAGE = "page"

    ROBOTS = ("index,follow", "noindex,follow", "index,nofollow", "noindex,nofollow")
    CHANGEFREQ = ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never")

    path = models.CharField(max_length=255, null=True, blank=True)
    entity_type = models.CharField(max_length=10, choices=Entity, null=True, blank=True)
    entity_id = models.BigIntegerField(null=True, blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    canonical_url = models.CharField(max_length=500, blank=True)
    robots = models.CharField(
        max_length=20, null=True, blank=True, choices=[(r, r) for r in ROBOTS]
    )
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=300, blank=True)
    og_image_url = models.CharField(max_length=500, blank=True)
    og_type = models.CharField(max_length=30, blank=True)
    twitter_card = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[("summary", "summary"), ("summary_large_image", "summary_large_image")],
    )
    structured_data = models.JSONField(null=True, blank=True)
    in_sitemap = models.BooleanField(default=True)
    sitemap_priority = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    sitemap_changefreq = models.CharField(
        max_length=10, null=True, blank=True, choices=[(c, c) for c in CHANGEFREQ]
    )

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "seo_pages"

    @property
    def title(self) -> str:
        """Shown in the Trash and typed to confirm a hard delete."""
        return self.path or f"{self.entity_type} {self.entity_id}"


class PageViewDaily(models.Model):
    day = models.DateField(primary_key=True)  # real key is (day, path); rows are read only
    path = models.CharField(max_length=255)
    views = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = "page_views_daily"
