import { api } from "../../../shared/api/client";
import styles from "./admin.module.css";

/** Edit / Activate-Deactivate / Move to Trash buttons for one row of any admin resource. */
export function RecordActions({ base, row, onChange, onEdit, children }) {
  async function run(action) {
    try {
      await api(`${base}/${row.id}/${action}/`, { method: "POST" });
      onChange();
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <div className={styles.actions}>
      {children}
      {onEdit && (
        <button className={`btn btn-outline ${styles.small}`} onClick={() => onEdit(row)}>
          Edit
        </button>
      )}
      <button
        className={`btn btn-outline ${styles.small}`}
        onClick={() => run(row.is_active ? "deactivate" : "activate")}
      >
        {row.is_active ? "Deactivate" : "Activate"}
      </button>
      <button
        className={`btn btn-outline ${styles.small} ${styles.danger}`}
        onClick={() => run("soft-delete")}
      >
        Trash
      </button>
    </div>
  );
}

export function StatusBadge({ row }) {
  if (!row.is_active) return <span className={`${styles.badge} ${styles.inactive}`}>inactive</span>;
  if (!row.status) return null;
  return <span className={`${styles.badge} ${styles[row.status] ?? ""}`}>{row.status}</span>;
}
