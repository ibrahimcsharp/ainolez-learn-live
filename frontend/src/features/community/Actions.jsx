import { useState } from "react";
import { api } from "../../shared/api/client";
import styles from "./Community.module.css";

export function LikeButton({ targetType, targetId, liked, count }) {
  const [state, setState] = useState({ liked, count });

  async function toggle() {
    const data = await api("/community/like/", { method: "POST", body: { target_type: targetType, target_id: targetId } });
    setState((s) => ({ liked: data.liked, count: s.count + (data.liked ? 1 : -1) }));
  }

  return (
    <button className={styles.action} aria-pressed={state.liked} onClick={toggle}>
      ♥ {state.count}
    </button>
  );
}

export function ReportButton({ targetType, targetId }) {
  const [done, setDone] = useState(false);

  async function report() {
    const reason = prompt("What is wrong with this? (spam, rude, wrong…)");
    if (!reason) return;
    await api("/community/report/", { method: "POST", body: { target_type: targetType, target_id: targetId, reason } });
    setDone(true);
  }

  if (done) return <span className="muted">Reported, thank you.</span>;
  return (
    <button className={styles.action} onClick={report}>
      Report
    </button>
  );
}
