import { Link } from "react-router";
import { useAuth } from "../../app/AuthProvider";
import { useApi } from "../../shared/hooks/useApi";
import styles from "./Dashboard.module.css";

const EVENT_LABELS = {
  lesson_completed: "Lesson completed",
  exercise_solved: "Exercise solved",
  quiz_passed: "Quiz passed",
  quiz_perfect: "Perfect quiz score",
  course_completed: "Course completed",
  streak_day: "Daily streak",
};

export function DashboardPage() {
  const { user } = useAuth();
  const { data } = useApi("/learner/dashboard/");
  if (!data) return <p className="page-loading">Loading…</p>;
  const { stats, courses, certificates } = data;

  return (
    <>
      <h1>Hi {user.full_name || user.username} 👋</h1>
      <div className={styles.stats}>
        <Stat value={stats.total_points} label="points" accent />
        <Stat value={`${stats.current_streak} 🔥`} label="day streak" />
        <Stat value={stats.lessons_completed} label="lessons done" />
        <Stat value={certificates.length} label="certificates" />
      </div>

      <section className={styles.section}>
        <h2>My courses</h2>
        {courses.length === 0 && (
          <p className="card">
            You have not started a course yet. <Link to="/courses">Browse the free courses</Link>.
          </p>
        )}
        {courses.map((course) => (
          <article key={course.course_id} className={`card ${styles.course}`}>
            <div className={styles.grow}>
              <Link to={`/${course.slug}`}>
                <h3>{course.title}</h3>
              </Link>
              <div className={styles.bar}>
                <span style={{ width: `${course.progress_percent}%` }} />
              </div>
              <span className="muted">
                {course.status === "completed" ? "Completed 🎓" : `${course.progress_percent}% complete`}
              </span>
            </div>
            {course.status !== "completed" && (
              <Link className="btn btn-primary" to={`/${course.slug}/${course.resume?.slug ?? ""}`}>
                {course.resume ? "Resume" : "Start"}
              </Link>
            )}
          </article>
        ))}
      </section>

      {certificates.length > 0 && (
        <section className={styles.section}>
          <h2>My certificates</h2>
          {certificates.map((cert) => (
            <article key={cert.code} className={`card ${styles.course}`}>
              <div className={styles.grow}>
                <h3>{cert.course_title}</h3>
                <span className="muted">
                  {cert.status === "pending_review" ? "Waiting for review" : cert.status}
                </span>
              </div>
              {cert.status === "issued" && (
                <Link className="btn btn-neon" to={`/certificates/${cert.code}`}>
                  View and share
                </Link>
              )}
            </article>
          ))}
        </section>
      )}

      <div className={styles.columns}>
        <section className={`card ${styles.section}`}>
          <h2>Badges</h2>
          {stats.badges.length === 0 && <p className="muted">Finish your first lesson to earn a badge.</p>}
          <ul className={styles.badges}>
            {stats.badges.map((badge) => (
              <li key={badge.name} title={badge.description}>
                <span>{badge.icon}</span>
                {badge.name}
              </li>
            ))}
          </ul>
        </section>
        <section className={`card ${styles.section}`}>
          <h2>Recent points</h2>
          {stats.recent_points.length === 0 && <p className="muted">No points yet.</p>}
          <ul className={styles.points}>
            {stats.recent_points.map((entry, i) => (
              <li key={i}>
                <span>{EVENT_LABELS[entry.event_key] ?? entry.event_key}</span>
                <strong>+{entry.points}</strong>
              </li>
            ))}
          </ul>
          <Link to="/leaderboard">See the leaderboard</Link>
        </section>
      </div>
    </>
  );
}

function Stat({ value, label, accent }) {
  return (
    <div className={`card ${styles.stat}`}>
      <span className={accent ? styles.accent : undefined}>{value}</span>
      <span className="muted">{label}</span>
    </div>
  );
}
