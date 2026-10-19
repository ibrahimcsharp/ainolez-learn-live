"""Content changes refresh the prerendered pages and the sitemap."""

from modules.catalog.events import CourseChanged, LessonChanged
from modules.community.events import PostApproved
from modules.seo import services
from shared.events import subscribe


@subscribe(LessonChanged)
@subscribe(CourseChanged)
@subscribe(PostApproved)
def content_changed(event) -> None:
    services.schedule_build()
