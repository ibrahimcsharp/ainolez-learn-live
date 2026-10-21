import { ArchiveRestore, Trash2, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import styles from "../shared/admin.module.css";

const RESOURCES = [
  ["Categories", "/admin/catalog/categories", (r) => r.name],
  ["Courses", "/admin/catalog/courses", (r) => r.title],
  ["Chapters", "/admin/catalog/chapters", (r) => r.title],
  ["Lessons", "/admin/catalog/lessons", (r) => r.title],
  ["Blocks", "/admin/catalog/blocks", (r) => `${r.type} block #${r.id}`],
  ["Learning paths", "/admin/catalog/paths", (r) => r.title],
  ["Quizzes", "/admin/assessment/quizzes", (r) => r.title],
  ["Questions", "/admin/assessment/questions", (r) => r.question_text],
  ["Badges", "/admin/gamification/badges", (r) => r.name],
  ["Points rules", "/admin/gamification/points-rules", (r) => r.event_key],
  ["Spaces", "/admin/community/spaces", (r) => r.name],
  ["FAQ", "/admin/assistant/faq", (r) => r.question],
  ["Knowledge", "/admin/assistant/sources", (r) => r.title],
  ["Pages", "/admin/website/pages", (r) => r.title],
  ["Menus", "/admin/website/menus", (r) => r.name],
  ["Menu links", "/admin/website/menu-items", (r) => r.label || `${r.target} (#${r.id})`],
  ["SEO pages", "/admin/seo/pages", (r) => r.url || `${r.entity_type} ${r.entity_id}`],
  ["Certificates", "/admin/certification/certificates", (r) => `${r.certificate_code} · ${r.learner_name}`],
  ["Media", "/admin/media/files", (r) => r.original_name],
];

export function TrashPage() {
  const [[label, base, nameOf], setResource] = useState(RESOURCES[0]);
  const list = useApi(`${base}/?trash=1&page_size=500`);
  const [deleting, setDeleting] = useState(null);

  async function restore(row) {
    try {
      await api(`${base}/${row.id}/restore/`, { method: "POST" });
      list.reload();
    } catch (err) {
      alert(err.message);
    }
  }

  const rows = list.data?.results ?? [];
  return (
    <>
      <h1>Trash</h1>
      <div className={styles.tabs}>
        {RESOURCES.map((resource) => (
          <button key={resource[0]} className={`btn btn-outline ${styles.small}`}
            aria-pressed={resource[0] === label} onClick={() => setResource(resource)}>
            {resource[0]}
          </button>
        ))}
      </div>
      {rows.length === 0 && <p className="muted">No {label.toLowerCase()} in the Trash.</p>}
      <table className={styles.table}>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td>
                {nameOf(row)}
                <div className="muted">Deleted {new Date(row.deleted_at).toLocaleString()}</div>
              </td>
              <td>
                <div className={styles.actions}>
                  <button className={`btn btn-outline ${styles.small}`} onClick={() => restore(row)}>
                    <ArchiveRestore /> Restore
                  </button>
                  <button className={`btn btn-outline ${styles.small} ${styles.danger}`} onClick={() => setDeleting(row)}>
                    <Trash2 /> Delete forever
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {deleting && (
        <HardDeleteDialog url={`${base}/${deleting.id}/hard/`} onClose={() => setDeleting(null)}
          onDeleted={() => { setDeleting(null); list.reload(); }} />
      )}
    </>
  );
}

/** Shows what will be removed and asks the admin to type the item name. */
function HardDeleteDialog({ url, onClose, onDeleted }) {
  const preview = useApi(url);
  const [typed, setTyped] = useState("");
  const [error, setError] = useState(null);
  const dialog = useRef(null);
  const confirmText = preview.data?.confirm_text;
  useEffect(() => {
    if (!dialog.current.open) dialog.current.showModal();
  }, []);

  async function remove(event) {
    event.preventDefault();
    try {
      await api(url, { method: "DELETE", body: { confirm: typed } });
      onDeleted();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <dialog ref={dialog} className={styles.dialog} onClose={onClose}>
      <form onSubmit={remove}>
        <h3>Delete forever?</h3>
        <p>This cannot be undone. It will permanently remove:</p>
        <ul>
          {Object.entries(preview.data?.will_delete ?? {}).map(([kind, count]) => (
            <li key={kind}>{count} {kind}</li>
          ))}
        </ul>
        <div className="field">
          <label htmlFor="confirm">Type <strong>{confirmText}</strong> to confirm</label>
          <input id="confirm" value={typed} onChange={(e) => setTyped(e.target.value)} autoComplete="off" />
        </div>
        {error && <p className="notice notice-error">{error}</p>}
        <div className={styles.actions}>
          <button type="button" className="btn btn-outline" onClick={() => dialog.current.close()}>
            <X /> Cancel
          </button>
          <button className="btn btn-primary" style={{ background: "var(--red-600)" }} disabled={typed !== confirmText}>
            <Trash2 /> Delete forever
          </button>
        </div>
      </form>
    </dialog>
  );
}
