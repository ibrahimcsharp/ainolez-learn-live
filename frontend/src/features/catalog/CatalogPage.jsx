import {
  ArrowRight,
  BookOpen,
  Braces,
  Clock,
  Database,
  FileCode2,
  Palette,
  Route,
  Search,
  Terminal,
  X,
} from "lucide-react";
import { Link, useSearchParams } from "react-router";
import { LoadingBar } from "../../shared/ui/Loader";
import { useCatalog } from "./catalog";
import styles from "./CatalogPage.module.css";

const LEVELS = ["beginner", "intermediate", "advanced"];
const ICONS = { html: FileCode2, css: Palette, javascript: Braces, python: Terminal, sql: Database };

export function CatalogPage() {
  const catalog = useCatalog();
  const [params, setParams] = useSearchParams();
  const category = params.get("category") ?? "";
  const level = params.get("level") ?? "";
  const query = params.get("q") ?? "";

  const set = (key, value) =>
    setParams(
      (previous) => {
        const next = new URLSearchParams(previous);
        if (value) next.set(key, value);
        else next.delete(key);
        return next;
      },
      { replace: true },
    );

  const all = catalog.data?.courses ?? [];
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  const shown = all.filter(
    (course) =>
      (!category || course.category.slug === category) &&
      (!level || course.level === level) &&
      words.every((word) =>
        `${course.title} ${course.short_description} ${course.category.name}`.toLowerCase().includes(word),
      ),
  );
  const topics = (catalog.data?.categories ?? [])
    .map((c) => ({ ...c, count: all.filter((course) => course.category.slug === c.slug).length }))
    .filter((c) => c.count > 0);
  const filtered = Boolean(category || level || query);

  return (
    <>
      {catalog.loading && <LoadingBar />}
      <header className={styles.hero}>
        <div className="container">
          <span className={styles.eyebrow}>Course catalog</span>
          <h1>Explore all courses</h1>
          <p className={styles.lead}>
            Hand-written lessons with live code, exercises, quizzes and a free certificate at the end.
          </p>
          <label className={styles.search}>
            <Search size={18} aria-hidden />
            <input
              type="search"
              placeholder="Search courses, e.g. Python lists"
              value={query}
              onChange={(event) => set("q", event.target.value)}
              aria-label="Search courses"
            />
          </label>
          <p className={styles.facts}>
            <span>{all.length || "…"} courses</span>
            <span>{topics.length || "…"} topics</span>
            <span>100% free</span>
          </p>
        </div>
      </header>

      <div className="container page-body">
        <div className={styles.toolbar}>
          <div className={styles.chips} role="group" aria-label="Topic">
            <button aria-pressed={!category} onClick={() => set("category", "")}>
              All topics <span>{all.length}</span>
            </button>
            {topics.map((c) => (
              <button
                key={c.slug}
                aria-pressed={category === c.slug}
                onClick={() => set("category", c.slug)}
                style={{ "--accent": c.color }}
              >
                <i aria-hidden /> {c.name} <span>{c.count}</span>
              </button>
            ))}
          </div>
          <select value={level} onChange={(event) => set("level", event.target.value)} aria-label="Level">
            <option value="">All levels</option>
            {LEVELS.map((l) => (
              <option key={l} value={l}>
                {l[0].toUpperCase() + l.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {catalog.data ? (
          <>
            <p className={styles.count} aria-live="polite">
              {shown.length === all.length ? `${all.length} courses` : `${shown.length} of ${all.length} courses`}
              {filtered && (
                <button onClick={() => setParams({}, { replace: true })}>
                  <X size={14} /> Clear filters
                </button>
              )}
            </p>
            {shown.length > 0 ? (
              <div className={styles.grid}>
                {shown.map((course) => (
                  <CourseCard key={course.slug} course={course} />
                ))}
              </div>
            ) : (
              <div className={styles.empty}>
                <Search size={28} />
                <h2>No courses match</h2>
                <p className="muted">Try another word or topic.</p>
                <button className="btn btn-primary" onClick={() => setParams({}, { replace: true })}>
                  Show all courses
                </button>
              </div>
            )}
          </>
        ) : catalog.error ? (
          <div className={styles.empty}>
            <h2>Courses could not be loaded</h2>
            <p className="muted">Check your connection and try again.</p>
            <button className="btn btn-primary" onClick={catalog.retry}>
              Try again
            </button>
          </div>
        ) : (
          <div className={styles.grid} role="status" aria-label="Loading courses">
            {Array.from({ length: 6 }, (_, i) => (
              <div key={i} className={styles.skeleton} aria-hidden>
                <span />
                <span />
                <span />
                <span />
              </div>
            ))}
          </div>
        )}

        {catalog.data?.paths.length > 0 && !filtered && (
          <section className={styles.paths}>
            <h2>Learning paths</h2>
            <p className="muted">Courses in a recommended order, from first steps to confident.</p>
            <div className={styles.pathGrid}>
              {catalog.data.paths.map((path) => (
                <article key={path.slug} className={styles.path}>
                  <span className={styles.pathIcon}>
                    <Route size={20} />
                  </span>
                  <h3>{path.title}</h3>
                  {path.description && <p className="muted">{path.description}</p>}
                  <ol>
                    {path.courses.map((course) => (
                      <li key={course.slug}>
                        <Link to={`/${course.slug}`}>{course.title}</Link>
                      </li>
                    ))}
                  </ol>
                </article>
              ))}
            </div>
          </section>
        )}
      </div>
    </>
  );
}

export function CourseCard({ course }) {
  const Icon = ICONS[course.language_key] ?? BookOpen;
  return (
    <Link to={`/${course.slug}`} className={styles.card} style={{ "--accent": course.category.color }}>
      {course.thumbnail_url ? (
        <img src={course.thumbnail_url} alt="" className={styles.thumb} loading="lazy" />
      ) : (
        <span className={styles.icon}>
          <Icon size={22} />
        </span>
      )}
      <span className={styles.category}>{course.category.name}</span>
      <h3>{course.title}</h3>
      <p className={styles.description}>{course.short_description}</p>
      <span className={styles.meta}>
        <span className={styles.level}>{course.level}</span>
        {course.lesson_count > 0 && (
          <span>
            <BookOpen size={14} /> {course.lesson_count} lessons
          </span>
        )}
        {course.estimated_minutes > 0 && (
          <span>
            <Clock size={14} /> {duration(course.estimated_minutes)}
          </span>
        )}
        <ArrowRight size={16} className={styles.arrow} />
      </span>
    </Link>
  );
}

function duration(minutes) {
  if (minutes < 60) return `${minutes} min`;
  const rounded = Math.round(minutes / 5) * 5;
  const hours = Math.floor(rounded / 60);
  const rest = rounded % 60;
  return rest ? `${hours} h ${rest} min` : `${hours} h`;
}
