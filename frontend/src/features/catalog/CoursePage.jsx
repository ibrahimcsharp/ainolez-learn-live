import { Link, useParams } from "react-router";
import { useAuth } from "../../app/AuthProvider";
import { useApi } from "../../shared/hooks/useApi";
import { SitePage } from "../website/SitePage";
import styles from "./Catalog.module.css";

export function CoursePage() {
  const { courseSlug } = useParams();
  const { user } = useAuth();
  const { data: course, error } = useApi(`/public/courses/${courseSlug}/`);
  const { data: progress } = useApi(user && course ? `/learner/courses/${course.id}/progress/` : null);
  if (error?.status === 404) return <SitePage slug={courseSlug} />; // no course here: maybe a page
  if (!course) return <p className="page-loading">{error ? error.message : "Loading…"}</p>;

  const first = course.chapters.flatMap((chapter) => chapter.lessons)[0];
  const next = progress?.resume ?? first;
  const done = new Set(progress?.completed_lesson_ids ?? []);
  return (
    <>
      <section className={styles.courseHero}>
        <div className="container">
          <span className={styles.category}>{course.category.name}</span>
          <h1>{course.title}</h1>
          <p>{course.short_description}</p>
          {progress?.enrolled && (
            <p>
              <span className={styles.bar}>
                <span style={{ width: `${progress.progress_percent}%` }} />
              </span>{" "}
              {progress.completed ? "Completed 🎓" : `${progress.progress_percent}% complete`}
            </p>
          )}
          {next && (
            <Link to={`/${course.slug}/${next.slug}`} className="btn btn-neon">
              {progress?.resume ? "Resume" : "Start the course"}
            </Link>
          )}
        </div>
      </section>
      <div className={`container ${styles.outline}`}>
        {course.intro_video_html && (
          // Built and escaped by the API from an allow-listed video link.
          <div className={`lesson-content ${styles.intro}`} dangerouslySetInnerHTML={{ __html: course.intro_video_html }} />
        )}
        {course.description && <p>{course.description}</p>}
        {course.chapters.map((chapter, index) => (
          <section key={chapter.title + index} className="card">
            <h3>
              {index + 1}. {chapter.title}
            </h3>
            {chapter.description && <p className="muted">{chapter.description}</p>}
            <ol>
              {chapter.lessons.map((lesson) => (
                <li key={lesson.slug}>
                  <Link to={`/${course.slug}/${lesson.slug}`}>{lesson.title}</Link>{" "}
                  {done.has(lesson.id) && "✓ "}
                  <span className="muted">· {lesson.estimated_minutes} min</span>
                </li>
              ))}
            </ol>
          </section>
        ))}
      </div>
    </>
  );
}
