"""Write use cases of the seo module."""

from datetime import timedelta

from django.db import connection
from django.utils import timezone

from modules.seo import content, resolver
from modules.seo.models import SeoPage, SeoSettings
from shared import audit, jobs
from shared.exceptions import ServiceError
from shared.models import Job

SETTING_FIELDS = (
    "site_name", "title_template", "default_description", "default_keywords",
    "default_image_url", "locale", "twitter_site", "facebook_app_id",
    "google_site_verification", "bing_site_verification", "organization_logo_url",
    "social_profiles", "allow_indexing", "robots_txt_extra",
)  # fmt: skip
URL_FIELDS = ("canonical_url", "og_image_url")
BUILD_JOB = "seo.build"


def update_settings(changes: dict, by) -> SeoSettings:
    site = resolver.settings_row()
    profiles = changes.get("social_profiles", site.social_profiles)
    if not isinstance(profiles, list) or not all(_is_url(p, absolute=True) for p in profiles):
        raise ServiceError("Social profiles must be a list of https:// links.", "bad_profiles")
    if "{title}" not in changes.get("title_template", site.title_template):
        raise ServiceError("The title template needs {title} in it.", "bad_template")
    for name in SETTING_FIELDS:
        if name in changes:
            setattr(site, name, changes[name])
    site.updated_by = by
    site.save()
    audit.record("seosettings.updated", actor=by, entity=site, after=changes)
    schedule_build()
    return site


def save_page(page: SeoPage | None, data: dict, by) -> SeoPage:
    """Create or edit a page's SEO. A course, lesson or post URL is stored by
    that item (entity), so the settings follow a slug change."""
    page = page or SeoPage()
    if "path" in data:
        _set_target(page, data.pop("path") or "")
    elif page.pk is None:
        raise ServiceError("Enter the page's path, e.g. /courses.", "no_path")
    for name in URL_FIELDS:
        if data.get(name) and not _is_url(data[name]):
            raise ServiceError("Use a full https:// link or a path starting with /.", "bad_url")
    extra = data.get("structured_data")
    if extra is not None and not _is_json_ld(extra):
        raise ServiceError(
            "Structured data must be a JSON-LD object or a list of them.", "bad_json"
        )
    for name, value in data.items():
        setattr(page, name, value)
    is_new = page.pk is None
    if is_new:
        page.created_by = by
    page.updated_by = by
    page.save()
    audit.record(f"seopage.{'created' if is_new else 'updated'}", actor=by, entity=page)
    schedule_build()
    return page


def record_view(path: str) -> None:
    """One more view of `path` today (cookie-free analytics)."""
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO page_views_daily (day, path, views) VALUES (%s, %s, 1) "
            "ON DUPLICATE KEY UPDATE views = views + 1",
            [timezone.now().date(), path[:255]],
        )


def schedule_build() -> None:
    """Rebuild the prerendered pages and sitemap in a minute, once for many edits."""
    queued = Job.objects.filter(type=BUILD_JOB, status=Job.Status.QUEUED).exists()
    if not queued:
        jobs.enqueue(BUILD_JOB, delay=timedelta(minutes=1))


def _set_target(page: SeoPage, raw_path: str) -> None:
    path = resolver.normalize(raw_path)
    if not resolver.SAFE_PATH.match(path):
        raise ServiceError(
            "Use a path like /courses: lowercase letters, numbers, - and /.", "bad_path"
        )
    if resolver.is_private(path):
        raise ServiceError("Admin and dashboard pages are never indexed.", "private_path")
    entity = content.entity_for_path(path)
    if entity:
        page.path = None
        page.entity_type, page.entity_id = entity
        same = {"entity_type": page.entity_type, "entity_id": page.entity_id}
    else:
        page.path, page.entity_type, page.entity_id = path, None, None
        same = {"path": path}
    if SeoPage.objects.exclude(pk=page.pk).filter(**same).exists():
        raise ServiceError("This page already has SEO settings. Edit those instead.", "duplicate")


def _is_url(value, absolute: bool = False) -> bool:
    if not isinstance(value, str):
        return False
    if value.startswith(("https://", "http://")):
        return True
    return not absolute and value.startswith("/")


def _is_json_ld(value) -> bool:
    items = value if isinstance(value, list) else [value]
    return all(isinstance(item, dict) and item for item in items)
