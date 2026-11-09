import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { useAuth } from "../../app/AuthProvider";
import { api, fromStatic } from "../../shared/api/client";
import { useApi } from "../../shared/hooks/useApi";
import { PageLoader } from "../../shared/ui/Loader";
import { SitePage } from "../website/SitePage";
import styles from "./Catalog.module.css";

export function CoursePage() {
  const { courseSlug } = useParams();
  const { user } = useAuth();
  const { course, isPage, error } = useCourseOrPage(courseSlug);
  const { data: progress } = useApi(user && course ? `/learner/courses/${course.id}/progress/` : null);
  if (isPage) return <SitePage slug={courseSlug} />; // no course here: maybe a page
  if (error) return <p className="page-loading">{error.message}</p>;
  if (!course) return <PageLoader />;

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
        {course.description_html && (
          // Markdown from the admin's smart editor, sanitised by the API.
          <div className="lesson-content" dangerouslySetInnerHTML={{ __html: course.description_html }} />
        )}
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

/**
 * Courses and site pages share /<slug>. The static copies answer which one it is at once;
 * only when neither has a copy (e.g. something published a moment ago) is the API asked.
 */
function useCourseOrPage(slug) {
  const [state, setState] = useState({ course: null, isPage: false, error: null });
  useEffect(() => {
    let live = true;
    setState({ course: null, isPage: false, error: null });
    const path = `/public/courses/${slug}/`;
    (async () => {
      const copy = await fromStatic(path);
      if (!copy && (await fromStatic(`/public/site/pages/${slug}/`))) return { isPage: true };
      try {
        return { course: copy ?? (await api(path)) };
      } catch (error) {
        return error.status === 404 ? { isPage: true } : { error };
      }
    })().then((result) => live && setState({ course: null, isPage: false, error: null, ...result }));
    return () => {
      live = false;
    };
  }, [slug]);
  return state;
}
