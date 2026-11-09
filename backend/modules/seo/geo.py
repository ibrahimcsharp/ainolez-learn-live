"""
GEO (generative engine optimisation): what AI engines read, and how well the site is set up
for them.

    llms.txt         the site in a few lines with links to every course and page
    llms-full.txt    every course and lesson as Markdown, in one file
    /python.md, /python/lists.md, /about.md
                     each course, lesson and page as clean Markdown (no app shell)
    robots.txt       AI crawlers the admin blocked (ai_bots)

Written by prerender.build, so Apache serves them as files (the API is slow on CGI).
"""

import re
from urllib.parse import urlparse

from modules.catalog import selectors as catalog
from modules.catalog import services as catalog_services
from modules.seo.content import absolute
from modules.seo.models import AiBot, SeoSettings
from modules.website import selectors as website

SHORTCODE = re.compile(r"^\{\{(youtube|vimeo|video):\s*(\S+?)\s*\}\}$", re.M)
TRYIT_FENCE = re.compile(r"^(\s*(?:`{3,}|~{3,})[\w+-]+)[ \t]+tryit[ \t]*$", re.M)  # ```python tryit
SEARCH_BOTS = ("OAI-SearchBot", "Claude-SearchBot", "PerplexityBot")
USER_BOTS = ("ChatGPT-User", "Claude-User", "Perplexity-User")


# --- Markdown copies ------------------------------------------------------------


def markdown_path(path: str) -> str:
    """/python/lists -> /python/lists.md"""
    return f"{path.rstrip('/')}.md"


def markdown_for(path: str, entity: tuple[str, int] | None) -> str | None:
    """The page at `path` as Markdown, or None for pages that have no Markdown copy."""
    kind = entity[0] if entity else ""
    parts = path.strip("/").split("/")
    if kind == "course" and len(parts) == 1:
        return _course_markdown(parts[0])
    if kind == "lesson" and len(parts) == 2:
        return _lesson_markdown(parts[0], parts[1])
    if kind == "page" and len(parts) == 1:
        return _page_markdown(parts[0])
    return None


def _course_markdown(slug: str) -> str | None:
    found = catalog.public_course(slug)
    if found is None:
        return None
    course, chapters = found
    lines = [f"# {course.title}", ""]
    if course.short_description:
        lines += [f"> {course.short_description}", ""]
    lines += [
        f"Free {course.level} course on ainolez. Page: {absolute('/' + course.slug)}",
        "",
    ]
    if course.description:
        lines += [_clean(course.description), ""]
    for chapter in chapters:
        lines += [f"## {chapter.title}", ""]
        lines += [
            f"- [{lesson.title}]({absolute(markdown_path(f'/{course.slug}/{lesson.slug}'))})"
            + (f": {lesson.summary}" if lesson.summary else "")
            for lesson in chapter.visible_lessons
        ]
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def _lesson_markdown(course_slug: str, lesson_slug: str) -> str | None:
    page = catalog.public_lesson(course_slug, lesson_slug)
    if page is None:
        return None
    lesson, course = page.lesson, page.lesson.course
    url = absolute(f"/{course.slug}/{lesson.slug}")
    lines = [f"# {lesson.title}", ""]
    if lesson.summary:
        lines += [f"> {lesson.summary}", ""]
    lines += [
        f"Lesson of the free course [{course.title}]({absolute('/' + course.slug)}) on ainolez."
        f" Page with live code editor: {url}",
        "",
        _clean(catalog_services.reader_markdown(page.blocks)),
        "",
    ]
    pager = [
        f"{label}: [{other.title}]({absolute(markdown_path(f'/{course.slug}/{other.slug}'))})"
        for label, other in (("Previous", page.previous), ("Next", page.next))
        if other
    ]
    if pager:
        lines += ["---", "", *pager]
    return "\n".join(lines).strip() + "\n"


def _page_markdown(slug: str) -> str | None:
    page = website.public_page(slug)
    if page is None or page.kind != "markdown":
        return None  # custom code pages have no Markdown
    lines = [f"# {page.title}", ""]
    if page.summary:
        lines += [f"> {page.summary}", ""]
    lines.append(_clean(page.content_md or ""))
    return "\n".join(lines).strip() + "\n"


def _clean(markdown: str) -> str:
    """Video shortcodes become links an AI engine can follow, and ```python tryit is plain
    ```python."""

    def link(match: re.Match) -> str:
        kind, value = match.groups()
        if kind == "youtube":
            value = f"https://www.youtube.com/watch?v={value}"
        elif kind == "vimeo":
            value = f"https://vimeo.com/{value}"
        return f"[Video]({value})"

    return TRYIT_FENCE.sub(r"\1", SHORTCODE.sub(link, markdown.strip()))


# --- llms.txt ---------------------------------------------------------------------


def llms_txt(site: SeoSettings, pages, copies: set[str]) -> str:
    """https://llmstxt.org: a short Markdown guide to the site for AI engines.
    `pages` are the resolved public pages (resolver.PageMeta), `copies` the paths that
    have a Markdown copy."""

    def link(meta) -> str:
        return absolute(markdown_path(meta.path)) if meta.path in copies else meta.canonical

    def item(meta) -> str:
        return f"- [{_plain_name(meta.title, site)}]({link(meta)})" + (
            f": {meta.description}" if meta.description else ""
        )

    shown = [meta for meta in pages if meta.indexable]
    courses = [meta for meta in shown if meta.entity and meta.entity[0] == "course"]
    site_pages = [meta for meta in shown if meta.entity and meta.entity[0] == "page"]
    lines = [f"# {site.site_name}", "", f"> {summary(site)}", ""]
    if site.geo_llms_details and site.geo_llms_details.strip():
        lines += [site.geo_llms_details.strip(), ""]
    lines += [
        "Every course is free, with lessons, live code examples, exercises, quizzes and a "
        "certificate."
        + (" Links ending in .md are Markdown copies of the pages." if copies else ""),
        "",
    ]
    if courses:
        lines += ["## Courses", "", *(item(meta) for meta in courses), ""]
    if site_pages:
        lines += ["## Pages", "", *(item(meta) for meta in site_pages), ""]
    lines += ["## Optional", ""]
    if site.geo_llms_full_enabled:
        lines.append(f"- [Every course and lesson in one file]({absolute('/llms-full.txt')})")
    lines += [
        f"- [All courses]({absolute('/courses')})",
        f"- [Community questions and answers]({absolute('/community')})",
        f"- [Sitemap]({absolute('/sitemap.xml')})",
    ]
    return "\n".join(lines).strip() + "\n"


def llms_full_txt(site: SeoSettings, pages, markdown: dict[str, str]) -> str:
    """Each course followed by its lessons, all as Markdown."""
    parts = [f"# {site.site_name}\n\n> {summary(site)}\n"]
    for meta in pages:
        if meta.indexable and meta.entity and meta.entity[0] == "course":
            found = catalog.public_course(meta.path.strip("/"))
            if found is None or meta.path not in markdown:
                continue
            course, chapters = found
            parts.append(markdown[meta.path])
            for chapter in chapters:
                for lesson in chapter.visible_lessons:
                    text = markdown.get(f"/{course.slug}/{lesson.slug}")
                    if text:
                        parts.append(text)
    return "\n\n---\n\n".join(part.strip() for part in parts) + "\n"


def summary(site: SeoSettings) -> str:
    return (site.geo_site_summary or site.default_description or site.site_name).strip()


def _plain_name(title: str, site: SeoSettings) -> str:
    """'Python · ainolez' -> 'Python' (the title template's suffix is noise here)."""
    template = site.title_template
    if "{title}" in template:
        before, after = template.split("{title}", 1)
        if before and title.startswith(before):
            title = title[len(before) :]
        if after and title.endswith(after):
            title = title[: -len(after)]
    return title


# --- AI crawlers ------------------------------------------------------------------


def bots() -> list[AiBot]:
    return list(AiBot.objects.filter(is_active=True).order_by("sort_order", "user_agent"))


def robots_lines() -> list[str]:
    """robots.txt groups that block the AI crawlers the admin turned off. A bot that
    is allowed needs no group: it follows the `User-agent: *` rules."""
    lines = []
    for bot in bots():
        if not bot.allowed:
            lines += ["", f"# {bot.owner}: {bot.notes or bot.purpose}".rstrip(),
                      f"User-agent: {bot.user_agent}", "Disallow: /"]  # fmt: skip
    if lines:
        lines.insert(0, "")
        lines.insert(1, "# AI crawlers blocked in Admin -> SEO & GEO -> AI crawlers")
    return lines


# --- where visitors come from -----------------------------------------------------

# (kind, source, host suffixes). Checked in order: gemini.google.com before google.
SOURCES = [
    ("ai", "ChatGPT", ("chatgpt.com", "chat.openai.com")),
    ("ai", "Perplexity", ("perplexity.ai",)),
    ("ai", "Claude", ("claude.ai",)),
    ("ai", "Gemini", ("gemini.google.com", "bard.google.com")),
    ("ai", "Copilot", ("copilot.microsoft.com", "copilot.cloud.microsoft")),
    ("ai", "DeepSeek", ("chat.deepseek.com",)),
    ("ai", "Grok", ("grok.com",)),
    ("ai", "Meta AI", ("meta.ai",)),
    ("ai", "Mistral", ("chat.mistral.ai",)),
    ("ai", "You.com", ("you.com",)),
    ("ai", "Phind", ("phind.com",)),
    ("search", "Google", ("google.com", "google.")),
    ("search", "Bing", ("bing.com",)),
    ("search", "DuckDuckGo", ("duckduckgo.com",)),
    ("search", "Yahoo", ("yahoo.com",)),
    ("search", "Yandex", ("yandex.ru", "yandex.com")),
    ("search", "Baidu", ("baidu.com",)),
    ("search", "Ecosia", ("ecosia.org",)),
    ("search", "Brave", ("search.brave.com",)),
    ("social", "LinkedIn", ("linkedin.com", "lnkd.in")),
    ("social", "Facebook", ("facebook.com", "fb.com")),
    ("social", "X", ("x.com", "twitter.com", "t.co")),
    ("social", "Reddit", ("reddit.com",)),
    ("social", "YouTube", ("youtube.com",)),
    ("social", "Instagram", ("instagram.com",)),
    ("social", "Hacker News", ("news.ycombinator.com",)),
]
# utm_source values AI apps add to links (ChatGPT adds utm_source=chatgpt.com)
UTM_NAMES = {"chatgpt": "ChatGPT", "openai": "ChatGPT", "perplexity": "Perplexity",
             "claude": "Claude", "gemini": "Gemini", "copilot": "Copilot"}  # fmt: skip


def classify(referrer: str = "", utm_source: str = "") -> tuple[str, str] | None:
    """('ai', 'ChatGPT'), ('search', 'Google') ... or None for other visits."""
    utm = (utm_source or "").strip().lower()
    if utm:
        found = _by_host(utm) or next(
            (("ai", name) for key, name in UTM_NAMES.items() if key in utm), None
        )
        if found:
            return found
    host = (urlparse(referrer or "").hostname or "").lower()
    return _by_host(host) if host else None


def _by_host(host: str) -> tuple[str, str] | None:
    host = host.removeprefix("www.").removeprefix("m.")
    for kind, name, suffixes in SOURCES:
        for suffix in suffixes:
            if suffix.endswith("."):  # google. = any Google country site
                if host.startswith(suffix) or f".{suffix}" in f".{host}":
                    return kind, name
            elif host == suffix or host.endswith(f".{suffix}"):
                return kind, name
    return None


# --- GEO checklist ----------------------------------------------------------------


def checks(site: SeoSettings) -> list[dict]:
    """What the site does for AI engines. Each: key, ok, label, tip, fix (a setting key
    the Center can switch on in one click, or "")."""
    by_agent = {bot.user_agent: bot for bot in bots()}
    blocked_search = [a for a in SEARCH_BOTS if a in by_agent and not by_agent[a].allowed]
    blocked_user = [a for a in USER_BOTS if a in by_agent and not by_agent[a].allowed]
    return [
        _check("indexing", site.allow_indexing, "Search engines may index the site",
               "Turn on 'Let search engines index the site' in Site defaults. "
               "AI search engines use the same signals.", "allow_indexing"),
        _check("llms", site.geo_llms_enabled, "llms.txt describes the site for AI engines",
               "A short Markdown guide at /llms.txt helps AI tools find the right pages.",
               "geo_llms_enabled"),
        _check("llms_full", site.geo_llms_full_enabled, "llms-full.txt has every lesson",
               "One file with every course and lesson, for AI tools that read whole sites.",
               "geo_llms_full_enabled"),
        _check("markdown", site.geo_markdown_copies, "Markdown copy of every page",
               "AI crawlers read plain Markdown far better than an app page.",
               "geo_markdown_copies"),
        _check("video", site.geo_video_moments, "Video key moments from timestamps",
               "Timestamps under videos become chapters Google and AI engines can cite.",
               "geo_video_moments"),
        _check("search_bots", not blocked_search, "AI search engines may read the site",
               "Blocked: " + ", ".join(blocked_search) + ". They decide what AI search shows."
               if blocked_search else "ChatGPT, Claude and Perplexity search can cite you.", ""),
        _check("user_bots", not blocked_user, "AI assistants may open pages people ask about",
               "Blocked: " + ", ".join(blocked_user) if blocked_user
               else "When someone shares a link with an assistant, it can read the page.", ""),
        _check("summary", bool(site.geo_site_summary.strip()), "A summary of the site for AI",
               "Write one or two sentences in AI & GEO: who the site is for and what it gives.",
               ""),
        _check("logo", bool(site.organization_logo_url), "Organization logo",
               "Add a square logo in Site defaults so engines show the right brand.", ""),
        _check("profiles", bool(site.social_profiles), "Links to social profiles",
               "Add your LinkedIn, YouTube and X profiles in Site defaults. Engines use them "
               "to recognise the brand.", ""),
        _check("indexnow", site.indexnow_enabled, "IndexNow tells Bing about changes",
               "Bing (which ChatGPT and Copilot search on) hears about new pages in minutes.",
               "indexnow_enabled"),
    ]  # fmt: skip


def _check(key: str, ok: bool, label: str, tip: str, fix: str) -> dict:
    return {"key": key, "ok": bool(ok), "label": label, "tip": tip, "fix": fix if not ok else ""}
