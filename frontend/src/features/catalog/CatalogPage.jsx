import { Link, useSearchParams } from "react-router";
import { useApi } from "../../shared/hooks/useApi";
import styles from "./Catalog.module.css";

export function CatalogPage() {
  const [params, setParams] = useSearchParams();
  const category = params.get("category") ?? "";
  const categories = useApi("/public/categories/");
  const courses = useApi(`/public/courses/?category=${encodeURIComponent(category)}`);
  const paths = useApi("/public/paths/");

  return (
    <div className="container" style={{ padding: "40px 16px 64px" }}>
      <h1>All courses</h1>
      <p className="muted">Every course is free. Pick a topic and start.</p>
      <div className={styles.filters}>
        <button aria-pressed={!category} onClick={() => setParams({})}>All</button>
        {(categories.data ?? []).map((c) => (
          <button key={c.slug} aria-pressed={category === c.slug} onClick={() => setParams({ category: c.slug })}>
            {c.icon} {c.name}
          </button>
        ))}
      </div>
      {courses.data?.length === 0 && <p className="muted">No courses here yet.</p>}
      <div className={styles.grid}>
        {(courses.data ?? []).map((course) => (
          <CourseCard key={course.slug} course={course} />
        ))}
      </div>

      {paths.data?.length > 0 && (
        <>
          <h2 style={{ marginTop: 48 }}>Learning paths</h2>
          {paths.data.map((path) => (
            <section key={path.slug} className={`card ${styles.path}`}>
              <h3>{path.title}</h3>
              <p className="muted">{path.description}</p>
              <ol>
                {path.courses.map((course) => (
                  <li key={course.slug}>
                    <Link to={`/${course.slug}`}>{course.title}</Link>
                  </li>
                ))}
              </ol>
            </section>
          ))}
        </>
      )}
    </div>
  );
}

export function CourseCard({ course }) {
  return (
    <Link to={`/${course.slug}`} className={`card ${styles.card}`} style={{ "--accent": course.category.color }}>
      {course.thumbnail_url && <img src={course.thumbnail_url} alt="" className={styles.thumb} />}
      <span className={styles.category}>{course.category.name}</span>
      <h3>{course.title}</h3>
      <p className="muted">{course.short_description}</p>
      <span className={styles.meta}>
        {course.level}
        {course.estimated_minutes > 0 && ` · ${Math.round(course.estimated_minutes / 60) || 1} h`}
      </span>
    </Link>
  );
}
