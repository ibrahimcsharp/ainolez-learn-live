import { Ban, Eye, Pencil, RotateCcw } from "lucide-react";
import { useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import styles from "../shared/admin.module.css";

const CERTIFICATES = "/admin/certification/certificates";
const TEMPLATES = "/admin/certification/templates";
const FILTERS = { "": "All", pending_review: "Waiting for review", issued: "Issued", revoked: "Revoked" };

/** Review certificates (approve, revoke, re-issue) and edit the certificate design. */
export function CertificatesPage() {
  const [status, setStatus] = useState("");
  const [query, setQuery] = useState("");
  const list = useApi(`${CERTIFICATES}/?page_size=200&status=${status}&q=${encodeURIComponent(query)}`);

  async function run(cert, action, body) {
    try {
      await api(`${CERTIFICATES}/${cert.id}/${action}/`, { method: "POST", body });
      list.reload();
    } catch (error) {
      alert(error.message);
    }
  }

  function revoke(cert) {
    const reason = prompt(`Why revoke ${cert.learner_name}'s certificate?`);
    if (reason) run(cert, "revoke", { reason });
  }

  return (
    <>
      <div className={styles.toolbar}>
        <h1>Certificates</h1>
        <input type="search" placeholder="Learner, course or ID" value={query} onChange={(e) => setQuery(e.target.value)} />
      </div>
      <div className={styles.tabs}>
        {Object.entries(FILTERS).map(([key, label]) => (
          <button key={key} className={`btn btn-outline ${styles.small}`} aria-pressed={status === key}
            onClick={() => setStatus(key)}>
            {label}
          </button>
        ))}
      </div>
      <table className={styles.table}>
        <thead>
          <tr><th>Learner</th><th>Course</th><th>Status</th><th>Views</th><th /></tr>
        </thead>
        <tbody>
          {(list.data?.results ?? []).map((cert) => (
            <tr key={cert.id}>
              <td>
                {cert.learner_name}
                <div className="muted"><code>{cert.certificate_code}</code></div>
              </td>
              <td>{cert.course_title}</td>
              <td>
                {cert.status}
                {cert.revoke_reason && <div className="muted">{cert.revoke_reason}</div>}
              </td>
              <td>{cert.view_count}</td>
              <td>
                <div className={styles.actions}>
                  {cert.status === "pending_review" && (
                    <button className={`btn btn-primary ${styles.small}`} onClick={() => run(cert, "approve")}>Approve</button>
                  )}
                  {cert.status === "issued" && (
                    <>
                      <a className={`btn btn-outline ${styles.small}`} href={cert.verify_url} target="_blank" rel="noreferrer"><Eye /> View</a>
                      <button className={`btn btn-outline ${styles.small} ${styles.danger}`} onClick={() => revoke(cert)}><Ban /> Revoke</button>
                    </>
                  )}
                  {cert.status !== "pending_review" && (
                    <button className={`btn btn-outline ${styles.small}`} onClick={() => run(cert, "reissue")}><RotateCcw /> Re-issue</button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <Templates />
    </>
  );
}

function Templates() {
  const list = useApi(`${TEMPLATES}/?page_size=50`);
  const [editing, setEditing] = useState(null);
  return (
    <section style={{ marginTop: 32 }}>
      <h2>Certificate design</h2>
      <p className="muted">Changes apply to new certificates, and to old ones when you re-issue them.</p>
      {editing && (
        <TemplateForm key={editing.id} initial={editing} onSaved={() => { setEditing(null); list.reload(); }}
          onCancel={() => setEditing(null)} />
      )}
      {(list.data?.results ?? []).map((template) => (
        <div key={template.id} className={`card ${styles.toolbar}`}>
          <span>
            <span style={{ background: template.primary_color, padding: "2px 10px", marginRight: 6 }} />
            <span style={{ background: template.accent_color, padding: "2px 10px", marginRight: 10 }} />
            <strong>{template.name}</strong> {template.is_default && "(default)"} · “{template.heading}”
          </span>
          <button className={`btn btn-outline ${styles.small}`} onClick={() => setEditing(template)}><Pencil /> Edit</button>
        </div>
      ))}
    </section>
  );
}

function TemplateForm({ initial, onSaved, onCancel }) {
  const form = useResourceForm(TEMPLATES, initial, onSaved);
  const { values, onChange, error } = form;
  const field = (label, name, props = {}) => (
    <Field label={label} name={name} value={values[name]} onChange={onChange} error={error} {...props} />
  );
  return (
    <EditPanel title="Edit design" form={form} onCancel={onCancel}>
      {field("Name", "name", { required: true })}
      {field("Heading", "heading")}
      {field("Line before the course name", "body_text")}
      {field("Signed by", "signer_name")}
      {field("Signer title", "signer_title")}
      {field("Main colour", "primary_color", { type: "color" })}
      {field("Accent colour", "accent_color", { type: "color" })}
    </EditPanel>
  );
}
