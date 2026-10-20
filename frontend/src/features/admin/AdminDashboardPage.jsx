import {
  Award,
  BookOpen,
  ClipboardCheck,
  FilePen,
  FileText,
  Flag,
  MessageSquareWarning,
  ShieldCheck,
  UserPlus,
  Users,
} from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "../../shared/api/client";
import styles from "./AdminDashboardPage.module.css";

const CARDS = [
  ["users", "learners", "Learners", Users],
  ["users", "new_learners_7d", "New learners this week", UserPlus],
  ["catalog", "courses_published", "Published courses", BookOpen],
  ["catalog", "lessons_published", "Published lessons", FileText],
  ["catalog", "lessons_draft", "Draft lessons", FilePen],
  ["certificates", "issued", "Certificates issued", Award],
  ["certificates", "pending_review", "Certificates to review", ClipboardCheck],
  ["community", "pending", "Posts and comments to approve", MessageSquareWarning],
  ["community", "open_reports", "Open reports", Flag],
  ["users", "admins", "Super admins", ShieldCheck],
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
      <p className="muted">A quick look at learners, content and what needs your attention.</p>
      {error && <p className="notice notice-error">{error.message}</p>}
      <div className={styles.grid}>
        {CARDS.map(([group, key, label, Icon]) => (
          <article key={key} className={`card ${styles.stat}`}>
            <span className={styles.icon}>
              <Icon size={20} />
            </span>
            <span className={styles.value}>{stats ? stats[group][key] : "–"}</span>
            <span className="muted">{label}</span>
          </article>
        ))}
      </div>
    </>
  );
}
