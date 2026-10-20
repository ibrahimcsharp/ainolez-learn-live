from modules.ai_authoring import services
from modules.ai_authoring.models import CourseJob
from shared.jobs import job


@job(services.OUTLINE_JOB)
def write_outline(payload: dict) -> None:
    course_job = CourseJob.objects.filter(pk=payload["job_id"]).first()
    if course_job and course_job.status == CourseJob.Status.OUTLINE_QUEUED:
        services.write_outline(course_job)


@job(services.LESSON_JOB)
def write_lesson(payload: dict) -> None:
    course_job = CourseJob.objects.filter(pk=payload["job_id"]).first()
    if course_job and course_job.status == CourseJob.Status.GENERATING:
        services.write_lesson(course_job, payload["lesson_id"])
