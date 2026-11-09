"""Write use cases of the seo module."""

import re
from datetime import timedelta

from django.db import connection
from django.utils import timezone

from modules.seo import changes as change_log
from modules.seo import content, geo, indexnow, resolver
from modules.seo.models import AiBot, SeoChangeLog, SeoPage, SeoSettings
from shared import audit, jobs
from shared.exceptions import ServiceError
from shared.models import Job

SETTING_FIELDS = (
    "site_name", "title_template", "default_description", "default_keywords",
    "default_image_url", "locale", "twitter_site", "facebook_app_id",
    "google_site_verification", "bing_site_verification", "organization_logo_url",
    "social_profiles", "allow_indexing", "robots_txt_extra",
    "geo_site_summary", "geo_llms_details", "geo_llms_enabled", "geo_llms_full_enabled",
    "geo_markdown_copies", "geo_video_moments", "indexnow_enabled",
)  # fmt: skip
BOT_FIELDS = ("user_agent", "owner", "purpose", "allowed", "notes", "sort_order")
USER_AGENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{1,59}$")
URL_FIELDS = ("canonical_url", "og_image_url")
BUILD_JOB = "seo.build"


def update_settings(changes: dict, by) -> SeoSettings:
    site = resolver.settings_row()
    profiles = changes.get("social_profiles", site.social_profiles)
    if not isinstance(profiles, list) or not all(_is_url(p, absolute=True) for p in profiles):
        raise ServiceError("Social profiles must be a list of https:// links.", "bad_profiles")
    if "{title}" not in changes.get("title_template", site.title_template):
        raise ServiceError("The title template needs {title} in it.", "bad_template")
    before = change_log.values(site, SETTING_FIELDS)
    for name in SETTING_FIELDS:
        if name in changes:
            setattr(site, name, changes[name])
    if site.indexnow_enabled and not site.indexnow_key:
        site.indexnow_key = indexnow.new_key()
    site.updated_by = by
    site.save()
    audit.record("seosettings.updated", actor=by, entity=site, after=changes)
    change_log.record(
        "settings",
        before=before,
        after={name: changes[name] for name in SETTING_FIELDS if name in changes},
        by=by,
        target="Site settings",
    )
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
    before = change_log.values(page, data.keys()) if page.pk else {}
    for name, value in data.items():
        setattr(page, name, value)
    is_new = page.pk is None
    if is_new:
        page.created_by = by
    page.updated_by = by
    page.save()
    audit.record(f"seopage.{'created' if is_new else 'updated'}", actor=by, entity=page)
    change_log.record(
        "page",
        before=before,
        after=change_log.values(page, data.keys()),
        by=by,
        target=page.path or f"{page.entity_type} {page.entity_id}",
        target_id=page.pk,
        summary="Added SEO settings" if is_new else "",
    )
    schedule_build()
    return page


def save_bot(bot: AiBot | None, data: dict, by) -> AiBot:
    """Add or change an AI crawler rule (robots.txt is rewritten by the next build)."""
    bot = bot or AiBot()
    agent = data.get("user_agent", bot.user_agent)
    if not USER_AGENT.match(agent or ""):
        raise ServiceError("Type the crawler's User-agent name, e.g. GPTBot.", "bad_agent")
    if AiBot.objects.exclude(pk=bot.pk).filter(user_agent__iexact=agent).exists():
        raise ServiceError(f"{agent} is already in the list.", "duplicate")
    if data.get("purpose", bot.purpose) not in AiBot.Purpose.values:
        raise ServiceError("Choose training, search or user.", "bad_purpose")
    is_new = bot.pk is None
    before = {} if is_new else change_log.values(bot, BOT_FIELDS)
    for name in BOT_FIELDS:
        if name in data:
            setattr(bot, name, data[name])
    if is_new:
        bot.created_by = by
    bot.updated_by = by
    bot.save()
    audit.record(f"aibot.{'created' if is_new else 'updated'}", actor=by, entity=bot)
    summary = ""
    if is_new:
        summary = f"Added crawler {bot.user_agent}"
    elif before["allowed"] != bot.allowed:
        summary = f"{'Allowed' if bot.allowed else 'Blocked'} {bot.user_agent}"
    change_log.record("ai_bot", before=before, after=change_log.values(bot, BOT_FIELDS), by=by,
                   target=bot.user_agent, target_id=bot.pk, summary=summary)  # fmt: skip
    schedule_build()
    return bot


def undo(entry: SeoChangeLog, by) -> SeoChangeLog:
    """Put back the old values of a logged admin change (logged again as a new change)."""
    if not change_log.can_undo(entry):
        raise ServiceError("This change cannot be undone.", "no_undo")
    old = {item["field"]: item["old"] for item in entry.changes}
    if entry.area == "settings":
        update_settings(old, by)
    elif entry.area == "page":
        page = SeoPage.all_objects.filter(pk=entry.target_id).first()
        if page is None or page.deleted_at:
            raise ServiceError("These page settings were deleted.", "gone")
        save_page(page, old, by)
    elif entry.area == "ai_bot":
        bot = AiBot.all_objects.filter(pk=entry.target_id).first()
        if bot is None or bot.deleted_at:
            raise ServiceError("This crawler was deleted.", "gone")
        save_bot(bot, old, by)
    entry.undone_at = timezone.now()
    entry.undone_by = by
    entry.save(update_fields=["undone_at", "undone_by"])
    return entry


def record_referral(path: str, referrer: str = "", utm_source: str = "") -> None:
    """Count a visit that came from a search engine, an AI engine or a social site."""
    found = geo.classify(referrer, utm_source)
    if found is None:
        return
    kind, source = found
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO referral_visits_daily (day, kind, source, path, visits) "
            "VALUES (%s, %s, %s, %s, 1) ON DUPLICATE KEY UPDATE visits = visits + 1",
            [timezone.now().date(), kind, source, path[:255]],
        )


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
