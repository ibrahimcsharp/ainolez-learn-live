from modules.certification import services
from modules.learning.events import CourseCompleted
from shared.events import subscribe


@subscribe(CourseCompleted)
def issue_certificate(event: CourseCompleted) -> None:
    services.issue_for_course(event.user_id, event.course_id)
