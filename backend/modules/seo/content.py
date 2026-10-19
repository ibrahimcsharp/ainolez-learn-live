"""
What a public page shows, as the facts SEO tags are built from: its name, a
description, an image, JSON-LD and a plain HTML copy of the main content
(for crawlers and link previews, before the React app starts).

Content is read through the other modules' selectors. Fixed pages that only
have an seo_pages row (e.g. /login) return None here.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime

from django.conf import settings
from django.utils.html import escape, strip_tags

from modules.catalog import selectors as catalog
from modules.certification import selectors as certification
from modules.community import selectors as community
from modules.media import selectors as media

POST_PATH = re.compile(r"^/community/posts/(\d+)$")
CERTIFICATE_PATH = re.compile(r"^/certificates/([A-Za-z0-9-]+)$")
COURSE_PATH = re.compile(r"^/([a-z0-9-]+)(?:/([a-z0-9-]+))?$")


@dataclass
class Content:
    name: str  # the page's own name; the title template is applied later
    description: str = ""
    image: str = ""
    og_type: str = "website"
    robots: str = ""  # default for this kind of page, e.g. noindex for certificates
    json_ld: list[dict] = field(default_factory=list)
    body_html: str = ""
    entity: tuple[str, int] | None = None
    updated_at: datetime | None = None


def for_path(path: str, site) -> Content | None:
    if path == "/":
        return _home(site)
    if path == "/courses":
        return Content(name="Courses", body_html=_course_list("All courses"))
    if path == "/community":
        return _community()
    if match := POST_PATH.match(path):
        return _post(int(match[1]))
    if match := CERTIFICATE_PATH.match(path):
        return _certificate(match[1])
    if match := COURSE_PATH.match(path):
        return _lesson(match[1], match[2]) if match[2] else _course(match[1], site)
    return None


def entity_for_path(path: str) -> tuple[str, int] | None:
    """The course, lesson or post a URL shows, drafts and pending posts included."""
    if match := POST_PATH.match(path):
        post_id = int(match[1])
        return ("post", post_id) if community.post_exists(post_id) else None
    if path != "/courses" and (match := COURSE_PATH.match(path)):
        return catalog.find_page(match[1], match[2] or "")
    return None


def absolute(url: str) -> str:
    if not url or url.startswith(("http://", "https://")):
        return url
    return settings.FRONTEND_URL.rstrip("/") + "/" + url.lstrip("/")


def snippet(html: str, limit: int = 160) -> str:
    """Plain text from HTML, cut at a word boundary."""
    text = " ".join(strip_tags(html or "").split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def organization(site) -> dict:
    org = {"@type": "Organization", "name": site.site_name, "url": absolute("/")}
    if site.organization_logo_url:
        org["logo"] = absolute(site.organization_logo_url)
    if site.social_profiles:
        org["sameAs"] = site.social_profiles
    return org


# --- page kinds ---------------------------------------------------------------


def _home(site) -> Content:
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site.site_name,
        "url": absolute("/"),
        "potentialAction": {
            "@type": "SearchAction",
            "target": absolute("/search") + "?q={search_term_string}",
            "query-input": "required name=search_term_string",
        },
    }
    return Content(
        name=site.site_name,
        json_ld=[website, {"@context": "https://schema.org", **organization(site)}],
        body_html=_course_list("Free coding and AI courses"),
    )


def _course_list(heading: str) -> str:
    items = "".join(
        f'<li><a href="/{c.slug}">{escape(c.title)}</a> {escape(c.short_description)}</li>'
        for c in catalog.public_courses()
    )
    return f"<h1>{escape(heading)}</h1><ul>{items}</ul>"


def _course(slug: str, site) -> Content | None:
    found = catalog.public_course(slug)
    if found is None:
        return None
    course, chapters = found
    url = absolute(f"/{course.slug}")
    description = course.short_description or snippet(course.description or "")
    data = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": course.title,
        "description": description,
        "url": url,
        "provider": organization(site),
        "isAccessibleForFree": True,
        "educationalLevel": course.level,
        "inLanguage": "en",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "category": "Free"},
        "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online"},
    }
    if course.estimated_minutes:
        data["hasCourseInstance"]["courseWorkload"] = f"PT{course.estimated_minutes}M"
    outline = "".join(
        f"<h2>{escape(chapter.title)}</h2><ul>"
        + "".join(
            f'<li><a href="/{course.slug}/{lesson.slug}">{escape(lesson.title)}</a></li>'
            for lesson in chapter.visible_lessons
        )
        + "</ul>"
        for chapter in chapters
    )
    thumbnail = media.urls_for([course.thumbnail_media_id]).get(course.thumbnail_media_id, "")
    return Content(
        name=course.title,
        description=description,
        image=thumbnail,
        json_ld=[data, _breadcrumbs([("Courses", "/courses"), (course.title, f"/{course.slug}")])],
        body_html=f"<h1>{escape(course.title)}</h1><p>{escape(description)}</p>{outline}",
        entity=("course", course.pk),
        updated_at=course.updated_at,
    )


def _lesson(course_slug: str, lesson_slug: str) -> Content | None:
    page = catalog.public_lesson(course_slug, lesson_slug)
    if page is None:
        return None
    lesson, course = page.lesson, page.lesson.course
    parts = []
    for block in page.blocks:
        if block.type in ("markdown", "callout"):
            parts.append(block.content_html or "")
        elif block.type == "example" and block.code_example:
            parts.append(f"<pre><code>{escape(block.code_example.starter_code)}</code></pre>")
    content_html = "".join(parts)
    description = lesson.summary or snippet(content_html)
    url = f"/{course.slug}/{lesson.slug}"
    data = {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": lesson.title,
        "description": description,
        "url": absolute(url),
        "learningResourceType": "Lesson",
        "isAccessibleForFree": True,
        "inLanguage": "en",
        "timeRequired": f"PT{lesson.estimated_minutes}M",
        "dateModified": lesson.updated_at.isoformat(),
        "isPartOf": {"@type": "Course", "name": course.title, "url": absolute(f"/{course.slug}")},
    }
    pager = "".join(
        f'<a href="/{course.slug}/{other.slug}">{label}: {escape(other.title)}</a> '
        for label, other in (("Previous", page.previous), ("Next", page.next))
        if other
    )
    trail = [("Courses", "/courses"), (course.title, f"/{course.slug}"), (lesson.title, url)]
    return Content(
        name=f"{lesson.title} · {course.title}",
        description=description,
        og_type="article",
        json_ld=[data, _breadcrumbs(trail)],
        body_html=(
            f'<p><a href="/{course.slug}">{escape(course.title)}</a></p>'
            f"<h1>{escape(lesson.title)}</h1>{content_html}<nav>{pager}</nav>"
        ),
        entity=("lesson", lesson.pk),
        updated_at=lesson.updated_at,
    )


def _community() -> Content:
    links = "".join(
        f'<li><a href="/community/posts/{p["id"]}">{escape(p["title"])}</a></li>'
        for p in community.posts()
    )
    return Content(name="Community", body_html=f"<h1>Community</h1><ul>{links}</ul>")


def _post(post_id: int) -> Content | None:
    post = community.post_detail(post_id, None)
    if post is None:
        return None
    url = absolute(f"/community/posts/{post_id}")
    data = {
        "@context": "https://schema.org",
        "@type": "DiscussionForumPosting",
        "headline": post["title"],
        "text": snippet(post["body_html"], 500),
        "url": url,
        "author": {"@type": "Person", "name": post["author"]},
        "datePublished": post["created_at"].isoformat(),
        "commentCount": post["reply_count"],
    }
    replies = "".join(f"<article>{r['body_html']}</article>" for r in post["replies"])
    return Content(
        name=post["title"],
        description=snippet(post["body_html"]),
        og_type="article",
        json_ld=[data],
        body_html=f"<h1>{escape(post['title'])}</h1>{post['body_html']}{replies}",
        entity=("post", post_id),
    )


def _certificate(code: str) -> Content | None:
    cert = certification.public_certificate(code)
    if cert is None:
        return None
    name = f"{cert.learner_name} completed {cert.course_title}"
    return Content(
        name=name,
        description=f"A free ainolez certificate for {cert.course_title}. Check it here.",
        image=cert.image_url,
        robots="noindex,follow",  # personal pages stay out of search results
        body_html=f"<h1>{escape(name)}</h1>",
    )


def _breadcrumbs(trail: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": absolute(url)}
            for i, (name, url) in enumerate(trail, start=1)
        ],
    }
