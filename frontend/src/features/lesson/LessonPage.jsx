import { useEffect, useState } from "react";
import { Link, NavLink, useParams } from "react-router";
import { useAuth } from "../../app/AuthProvider";
import { useAssistant } from "../assistant/AssistantProvider";
import { LessonComments } from "../community/LessonComments";
import { NotFound } from "../../app/NotFound";
import { api } from "../../shared/api/client";
import { useApi } from "../../shared/hooks/useApi";
import { CourseCompleteDialog } from "./CourseCompleteDialog";
import { LessonContent } from "./LessonContent";
import styles from "./LessonPage.module.css";

/** W3Schools-style lesson: topic sidebar on the left, Previous / Next buttons. */
export function LessonPage() {
  const { courseSlug, lessonSlug } = useParams();
  const { user } = useAuth();
  const { data: page, error } = useApi(`/public/courses/${courseSlug}/lessons/${lessonSlug}/`);
  const progress = useLearnerProgress(user, page?.lesson.id);
  useLessonForAssistant(page?.lesson.id);
  if (error?.status === 404) return <NotFound />;
  if (!page) return <p className={error ? "page-loading" : "page-loading is-loading"}>{error ? error.message : "Loading…"}</p>;

  const done = new Set(progress.state?.course.completed_lesson_ids ?? []);
  const pager = (
    <nav className={styles.pager} aria-label="Lesson navigation">
      {page.previous ? (
        <Link className="btn btn-primary" to={`/${courseSlug}/${page.previous.slug}`}>
          ❮ Previous
        </Link>
      ) : (
        <span />
      )}
      {page.next && (
        <Link className="btn btn-primary" to={`/${courseSlug}/${page.next.slug}`}>
          Next ❯
        </Link>
      )}
    </nav>
  );

  return (
    <div className={styles.layout}>
      <aside className={styles.sidebar}>
        <Link to={`/${courseSlug}`} className={styles.courseTitle}>
          {page.course.title}
        </Link>
        {progress.state && (
          <div className={styles.progress} title={`${progress.state.course.progress_percent}% complete`}>
            <span style={{ width: `${progress.state.course.progress_percent}%` }} />
          </div>
        )}
        {page.chapters.map((chapter, index) => (
          <div key={chapter.title + index}>
            <h4>{chapter.title}</h4>
            {chapter.lessons.map((lesson) => (
              <NavLink key={lesson.slug} to={`/${courseSlug}/${lesson.slug}`}>
                {done.has(lesson.id) && <span className={styles.tick}>✓</span>}
                {lesson.title}
              </NavLink>
            ))}
          </div>
        ))}
      </aside>
      <article className={styles.main}>
        {pager}
        <h1>{page.lesson.title}</h1>
        <LessonContent
          key={page.lesson.id}
          blocks={page.blocks}
          learner={{
            loggedIn: Boolean(user),
            solvedIds: new Set(progress.state?.solved_exercise_ids ?? []),
            quizResults: progress.state?.quiz_results ?? {},
            onProgress: progress.update,
          }}
        />
        <hr />
        <div className={styles.complete}>
          {!user ? (
            <Link to="/login">Log in to save your progress and earn points</Link>
          ) : done.has(page.lesson.id) ? (
            <span className={styles.tick}>✓ Lesson completed</span>
          ) : (
            <button className="btn btn-neon" onClick={progress.completeLesson}>
              Mark lesson complete
            </button>
          )}
        </div>
        {pager}
        <LessonComments lessonId={page.lesson.id} />
      </article>
      {progress.courseCompleted && (
        <CourseCompleteDialog courseTitle={page.course.title} onClose={progress.closeDialog} />
      )}
    </div>
  );
}

/** The logged-in learner's state for this lesson, and the actions that change it. */
function useLearnerProgress(user, lessonId) {
  const [state, setState] = useState(null);
  const [courseCompleted, setCourseCompleted] = useState(false);

  useEffect(() => {
    if (!user || !lessonId) return;
    api(`/learner/lessons/${lessonId}/visit/`, { method: "POST" }).then(setState).catch(() => {});
  }, [user, lessonId]);

  function update(result) {
    if (result.just_completed) setCourseCompleted(true);
    api(`/learner/lessons/${lessonId}/visit/`, { method: "POST" }).then(setState);
  }

  async function completeLesson() {
    update(await api(`/learner/lessons/${lessonId}/complete/`, { method: "POST" }));
  }

  return { state, update, completeLesson, courseCompleted, closeDialog: () => setCourseCompleted(false) };
}

/** While a lesson is open, the AI tutor answers with that lesson in mind. */
function useLessonForAssistant(lessonId) {
  const assistant = useAssistant();
  const setLessonId = assistant?.setLessonId;
  useEffect(() => {
    if (!setLessonId || !lessonId) return undefined;
    setLessonId(lessonId);
    return () => setLessonId(null);
  }, [setLessonId, lessonId]);
}
