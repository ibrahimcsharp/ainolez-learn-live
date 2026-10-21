import { useState } from "react";
import { useApi } from "../../shared/hooks/useApi";
import styles from "./Leaderboard.module.css";

const PERIODS = { week: "This week", month: "This month", all: "All time" };

export function LeaderboardPage() {
  const [period, setPeriod] = useState("week");
  const { data } = useApi(`/public/leaderboard/?period=${period}`);
  const leaders = data?.leaders ?? [];

  return (
    <div className="container page-body" style={{ maxWidth: "calc(720px + 2 * var(--gutter))" }}>
      <h1>Leaderboard</h1>
      <p className="muted">Earn points by finishing lessons, solving exercises and passing quizzes.</p>
      <div className={styles.tabs}>
        {Object.entries(PERIODS).map(([key, label]) => (
          <button key={key} aria-pressed={period === key} onClick={() => setPeriod(key)}>
            {label}
          </button>
        ))}
      </div>
      {data && leaders.length === 0 && <p className="muted">No points yet. Be the first!</p>}
      <ol className={styles.list}>
        {leaders.map((leader) => (
          <li key={leader.rank} className="card">
            <span className={styles.rank}>{["🥇", "🥈", "🥉"][leader.rank - 1] ?? leader.rank}</span>
            <span className={styles.name}>{leader.name}</span>
            <span className={styles.points}>{leader.points} pts</span>
          </li>
        ))}
      </ol>
    </div>
  );
}
