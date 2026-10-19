import { useEffect, useState } from "react";
import { api } from "../../shared/api/client";
import styles from "./AdminDashboardPage.module.css";

const CARDS = [
  ["users", "learners", "Learners"],
  ["users", "new_learners_7d", "New learners this week"],
  ["catalog", "courses_published", "Published courses"],
  ["catalog", "lessons_published", "Published lessons"],
  ["catalog", "lessons_draft", "Draft lessons"],
  ["certificates", "issued", "Certificates issued"],
  ["certificates", "pending_review", "Certificates to review"],
  ["community", "pending", "Posts and comments to approve"],
  ["community", "open_reports", "Open reports"],
  ["users", "admins", "Super admins"],
];

export function AdminDashboardPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api("/admin/platform/dashboard/").then(setStats).catch(setError);
  }, []);

  return (
    <>
      <h1>Dashboard</h1>
      {error && <p className="notice notice-error">{error.message}</p>}
      <div className={styles.grid}>
        {CARDS.map(([group, key, label]) => (
          <article key={key} className={`card ${styles.stat}`}>
            <span className={styles.value}>{stats ? stats[group][key] : "–"}</span>
            <span className="muted">{label}</span>
          </article>
        ))}
      </div>
    </>
  );
}
