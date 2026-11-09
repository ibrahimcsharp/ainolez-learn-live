"""Tables from database/schema/0011_seo.sql and 0022_seo_geo.sql."""

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
    # GEO: what AI engines get (0022)
    geo_site_summary = models.CharField(max_length=500, blank=True)
    geo_llms_details = models.TextField(null=True, blank=True)
    geo_llms_enabled = models.BooleanField(default=True)
    geo_llms_full_enabled = models.BooleanField(default=True)
    geo_markdown_copies = models.BooleanField(default=True)
    geo_video_moments = models.BooleanField(default=True)
    indexnow_enabled = models.BooleanField(default=False)
    indexnow_key = models.CharField(max_length=64, blank=True)
    indexnow_last_at = models.DateTimeField(null=True, blank=True)
    indexnow_last_result = models.CharField(max_length=300, blank=True)
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


class AiBot(BaseModel):
    """An AI crawler and whether robots.txt lets it read the site."""

    class Purpose(models.TextChoices):
        TRAINING = "training"
        SEARCH = "search"
        USER = "user"

    user_agent = models.CharField(max_length=60)
    owner = models.CharField(max_length=60, blank=True)
    purpose = models.CharField(max_length=10, choices=Purpose)
    allowed = models.BooleanField(default=True)
    notes = models.CharField(max_length=300, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "ai_bots"

    @property
    def title(self) -> str:
        return self.user_agent


class ReferralVisitDaily(models.Model):
    """Visits from search engines, AI engines and social sites. The real key is
    (day, kind, source, path); rows are written with SQL and only read here."""

    day = models.DateField(primary_key=True)
    kind = models.CharField(max_length=10)
    source = models.CharField(max_length=40)
    path = models.CharField(max_length=255)
    visits = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = "referral_visits_daily"


class SeoChangeLog(models.Model):
    class Actor(models.TextChoices):
        ADMIN = "admin"
        AUTO = "auto"

    created_at = models.DateTimeField(auto_now_add=True)
    actor = models.CharField(max_length=10, choices=Actor)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        db_column="user_id",
    )
    area = models.CharField(max_length=40)
    target = models.CharField(max_length=255, blank=True)
    target_id = models.BigIntegerField(null=True)
    summary = models.CharField(max_length=500, blank=True)
    changes = models.JSONField(null=True)
    undone_at = models.DateTimeField(null=True)
    undone_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        db_column="undone_by",
    )

    class Meta:
        managed = False
        db_table = "seo_change_log"
