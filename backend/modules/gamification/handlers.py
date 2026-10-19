"""Turns learning and community events into points, streaks and badges."""

from modules.community.events import PostApproved, ReplyMarkedHelpful
from modules.gamification import services
from modules.learning.events import CourseCompleted, ExerciseSolved, LessonCompleted, QuizPassed
from shared.events import subscribe


@subscribe(LessonCompleted)
def on_lesson_completed(event: LessonCompleted) -> None:
    services.record_activity(event.user_id)
    services.count(event.user_id, "lessons_completed")
    services.award(event.user_id, "lesson_completed", "lesson", event.lesson_id)
    services.check_badges(event.user_id)


@subscribe(ExerciseSolved)
def on_exercise_solved(event: ExerciseSolved) -> None:
    services.record_activity(event.user_id)
    services.award(event.user_id, "exercise_solved", "exercise", event.exercise_id)
    services.check_badges(event.user_id)


@subscribe(QuizPassed)
def on_quiz_passed(event: QuizPassed) -> None:
    services.record_activity(event.user_id)
    services.award(event.user_id, "quiz_passed", "quiz", event.quiz_id)
    if event.percentage >= 100:
        services.award(event.user_id, "quiz_perfect", "quiz", event.quiz_id)
    services.check_badges(event.user_id)


@subscribe(CourseCompleted)
def on_course_completed(event: CourseCompleted) -> None:
    services.count(event.user_id, "courses_completed")
    services.award(event.user_id, "course_completed", "course", event.course_id)
    services.check_badges(event.user_id)


@subscribe(PostApproved)
def on_post_approved(event: PostApproved) -> None:
    services.award(event.user_id, "first_post", "user", event.user_id)  # once per person
    services.check_badges(event.user_id)


@subscribe(ReplyMarkedHelpful)
def on_reply_marked_helpful(event: ReplyMarkedHelpful) -> None:
    services.award(event.user_id, "helpful_answer", "reply", event.reply_id)
    services.check_badges(event.user_id)
