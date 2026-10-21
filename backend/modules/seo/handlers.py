"""Content changes refresh the prerendered pages and the sitemap."""

from modules.catalog.events import CourseChanged, LessonChanged
from modules.community.events import PostApproved
from modules.seo import services
from modules.website.events import MenuChanged, PageChanged
from shared.events import subscribe


@subscribe(LessonChanged)
@subscribe(CourseChanged)
@subscribe(PostApproved)
@subscribe(PageChanged)
@subscribe(MenuChanged)  # every prerendered page carries the menus
def content_changed(event) -> None:
    services.schedule_build()
