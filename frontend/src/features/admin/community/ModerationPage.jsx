import { Ban, Check, EyeOff, Plus, Save, X } from "lucide-react";
import { useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { Field, FormError } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import { SortableList } from "../shared/SortableList";
import styles from "../shared/admin.module.css";

const ADMIN = "/admin/community";
const LABELS = { post: "Post", reply: "Reply", comment: "Lesson comment" };

/** Approve or reject waiting content, handle reports, manage spaces. */
export function ModerationPage() {
  const queue = useApi(`${ADMIN}/queue/`);

  async function moderate(item, action) {
    const reason = ["reject", "hide", "ban"].includes(action) ? prompt(`Reason to ${action}?`) : "";
    if (reason === null) return false;
    try {
      await api(`${ADMIN}/moderate/`, {
        method: "POST",
        body: { target_type: item.target_type, target_id: item.target_id ?? item.id, action, reason },
      });
      queue.reload();
      return true;
    } catch (error) {
      alert(error.message);
      return false;
    }
  }

  async function resolve(report, dismiss) {
    await api(`${ADMIN}/reports/${report.id}/resolve/`, { method: "POST", body: { dismiss } });
    queue.reload();
  }

  const pending = queue.data?.pending ?? [];
  const reports = queue.data?.reports ?? [];
  return (
    <>
      <h1>Community moderation</h1>
      <h2>Waiting for approval ({pending.length})</h2>
      {pending.length === 0 && <p className="muted">Nothing waiting. 🎉</p>}
      {pending.map((item) => (
        <article key={`${item.target_type}${item.id}`} className={`card ${styles.panel}`}>
          <p className="muted">
            {LABELS[item.target_type]} by <strong>{item.author}</strong> · {new Date(item.created_at).toLocaleString()}
          </p>
          {item.blocked_words.length > 0 && (
            <p className="notice notice-error">Uses blocked words: {item.blocked_words.join(", ")}</p>
          )}
          {item.title && <h3>{item.title}</h3>}
          <div className="lesson-content" dangerouslySetInnerHTML={{ __html: item.body_html }} />
          <div className={styles.actions} style={{ justifyContent: "flex-start" }}>
            <button className="btn btn-primary" onClick={() => moderate(item, "approve")}><Check /> Approve</button>
            <button className="btn btn-outline" onClick={() => moderate(item, "reject")}><X /> Reject</button>
            <button className={`btn btn-outline ${styles.danger}`} onClick={() => moderate(item, "ban")}>
              <Ban /> Hide and ban author
            </button>
          </div>
        </article>
      ))}

      <h2>Reports ({reports.length})</h2>
      {reports.length === 0 && <p className="muted">No open reports.</p>}
      {reports.map((report) => (
        <article key={report.id} className={`card ${styles.panel}`}>
          <p>
            <strong>{LABELS[report.target_type]}</strong> reported: “{report.reason}” · status {report.target_status}
          </p>
          <div className="lesson-content" dangerouslySetInnerHTML={{ __html: report.target_html }} />
          <div className={styles.actions} style={{ justifyContent: "flex-start" }}>
            <button className="btn btn-outline"
              onClick={async () => (await moderate(report, "hide")) && resolve(report, false)}>
              <EyeOff /> Hide it
            </button>
            <button className="btn btn-outline" onClick={() => resolve(report, true)}><X /> Dismiss</button>
          </div>
        </article>
      ))}

      <BlockedWords />
      <Spaces />
    </>
  );
}

function BlockedWords() {
  const { data } = useApi(`${ADMIN}/settings/`);
  const [values, setValues] = useState(null);
  const [state, setState] = useState({ saving: false, saved: false, error: null });
  const form = values ?? data;
  if (!form) return null;

  const onChange = (event) => {
    setValues({ ...form, [event.target.name]: event.target.value });
    setState({ saving: false, saved: false, error: null });
  };
  async function save(event) {
    event.preventDefault();
    setState({ saving: true, saved: false, error: null });
    try {
      setValues(await api(`${ADMIN}/settings/`, { method: "PATCH", body: form }));
      setState({ saving: false, saved: true, error: null });
    } catch (error) {
      setState({ saving: false, saved: false, error });
    }
  }

  return (
    <section style={{ marginTop: 32 }}>
      <h2>Blocked words</h2>
      <form className={`card ${styles.panel}`} onSubmit={save}>
        <p className="muted">
          One word or phrase per line. Posts, replies and lesson comments are checked for whole words,
          ignoring capitals and extra spaces. Admins are not checked.
        </p>
        <Field label="Blocked words and phrases" name="blocked_words" as="textarea" rows={8}
          value={form.blocked_words} onChange={onChange} error={state.error} />
        <Field label="When a text uses one" name="blocked_action" as="select"
          value={form.blocked_action} onChange={onChange} error={state.error}>
          <option value="hold">Save it, but hold it for approval (shown above with the words)</option>
          <option value="refuse">Refuse it and ask the writer to change the words</option>
        </Field>
        <FormError error={state.error} />
        <div className={styles.actions} style={{ justifyContent: "flex-start" }}>
          <button className="btn btn-primary" disabled={state.saving}>
            <Save /> {state.saving ? "Saving…" : "Save"}
          </button>
          {state.saved && <span className="muted">Saved.</span>}
        </div>
      </form>
    </section>
  );
}

function Spaces() {
  const BASE = `${ADMIN}/spaces`;
  const list = useApi(`${BASE}/?page_size=100`);
  const [editing, setEditing] = useState(null);
  const blank = { name: "", slug: "", description: "", icon: "💬", posting_rule: "open" };
  return (
    <section style={{ marginTop: 32 }}>
      <div className={styles.toolbar}>
        <h2>Spaces</h2>
        <button className="btn btn-primary" onClick={() => setEditing(blank)}><Plus /> New space</button>
      </div>
      {editing && (
        <SpaceForm key={editing.id ?? "new"} base={BASE} initial={editing}
          onSaved={() => { setEditing(null); list.reload(); }} onCancel={() => setEditing(null)} />
      )}
      <SortableList items={list.data?.results ?? []} base={BASE} onChange={list.reload}
        renderItem={(space) => (
          <div className={styles.toolbar} style={{ margin: 0 }}>
            <span>
              {space.icon} <strong>{space.name}</strong>{" "}
              {space.posting_rule === "approval_required" && <span className="muted">(every post approved)</span>}{" "}
              <StatusBadge row={space} />
            </span>
            <RecordActions base={BASE} row={space} onChange={list.reload} onEdit={setEditing} />
          </div>
        )} />
    </section>
  );
}

function SpaceForm({ base, initial, onSaved, onCancel }) {
  const form = useResourceForm(base, initial, onSaved);
  const { values, onChange, error } = form;
  return (
    <EditPanel title={initial.id ? "Edit space" : "New space"} form={form} onCancel={onCancel}>
      <Field label="Name" name="name" required value={values.name} onChange={onChange} error={error} />
      <Field label="Icon (emoji)" name="icon" value={values.icon} onChange={onChange} error={error} />
      <Field label="Posting" name="posting_rule" as="select" value={values.posting_rule} onChange={onChange}>
        <option value="open">Trusted members post straight away</option>
        <option value="approval_required">Every post needs approval</option>
      </Field>
      <Field label="Description" name="description" value={values.description} onChange={onChange} error={error} />
    </EditPanel>
  );
}
