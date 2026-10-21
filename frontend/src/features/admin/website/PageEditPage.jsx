import { ArrowLeft, ExternalLink, Power, PowerOff, Trash2 } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { MarkdownEditor } from "../shared/MarkdownEditor";
import { StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";
import { SeoEditor } from "../seo/SeoEditor";
import { PAGES } from "./PagesPage";

const BLANK = { title: "", slug: "", summary: "", content_md: "" };
const TABS = { content: "Content", seo: "SEO" };

/** Write a new page (/admin/pages/new) or edit one. */
export function PageEditPage() {
  const { id } = useParams();
  const isNew = id === "new";
  const page = useApi(isNew ? null : `${PAGES}/${id}/`);
  const navigate = useNavigate();
  const [tab, setTab] = useState("content");
  const [saved, setSaved] = useState("");

  if (!isNew && !page.data) return <p className="page-loading">{page.error?.message ?? "Loading…"}</p>;
  const data = page.data;

  function onSaved(row) {
    setSaved(`Saved at ${new Date().toLocaleTimeString()}.`);
    if (isNew) navigate(`/admin/pages/${row.id}`, { replace: true });
    else page.reload();
  }

  async function run(action) {
    try {
      await api(`${PAGES}/${data.id}/${action}/`, { method: "POST" });
      if (action === "soft-delete") navigate("/admin/pages");
      else page.reload();
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <>
      <Link to="/admin/pages" className={styles.back}>
        <ArrowLeft size={16} /> All pages
      </Link>
      <div className={styles.toolbar}>
        <div>
          <h1>{isNew ? "New page" : data.title}</h1>
          {data && (
            <>
              <span className="muted">/{data.slug}</span> <StatusBadge row={data} />
              {data.is_active ? <span className="muted"> · live on the site</span> : null}
            </>
          )}
        </div>
        {data && (
          <div className={styles.actions}>
            {saved && <span className="muted">{saved}</span>}
            {data.is_active && (
              <a className="btn btn-outline" href={`/${data.slug}`} target="_blank" rel="noreferrer">
                <ExternalLink /> View on site
              </a>
            )}
            <button className="btn btn-outline" onClick={() => run(data.is_active ? "deactivate" : "activate")}>
              {data.is_active ? <><PowerOff /> Hide</> : <><Power /> Show on site</>}
            </button>
            <button className={`btn btn-outline ${styles.danger}`} onClick={() => run("soft-delete")}>
              <Trash2 /> Trash
            </button>
          </div>
        )}
      </div>
      {data && (
        <div className={styles.tabs} role="tablist">
          {Object.entries(TABS).map(([key, label]) => (
            <button key={key} role="tab" className={`btn btn-outline ${styles.small}`} aria-pressed={tab === key}
              onClick={() => setTab(key)}>
              {label}
            </button>
          ))}
        </div>
      )}
      {/* Kept mounted on the SEO tab, so unsaved text is not lost. */}
      <div hidden={tab !== "content"}>
        <PageForm key={data?.updated_at ?? "new"} initial={data ?? BLANK} onSaved={onSaved} />
      </div>
      {tab === "seo" && data && (
        <section className="card">
          <SeoEditor key={data.slug} path={`/${data.slug}`} />
        </section>
      )}
    </>
  );
}

function PageForm({ initial, onSaved }) {
  const form = useResourceForm(PAGES, initial, onSaved, (v) => ({
    title: v.title, slug: v.slug, summary: v.summary, content_md: v.content_md,
  }));
  const { values, onChange, error } = form;
  return (
    <EditPanel form={form}>
      <Field label="Title" name="title" required value={values.title} onChange={onChange} error={error}
        placeholder="About ainolez" />
      <Field label="Web address (/slug, blank = from the title)" name="slug" value={values.slug} onChange={onChange}
        error={error} placeholder="about" />
      <div style={{ gridColumn: "1 / -1" }}>
        <Field label="Summary (shown by Google and in link previews)" name="summary" value={values.summary}
          onChange={onChange} error={error} maxLength={300} />
      </div>
      <MarkdownEditor name="content_md" label="Content" value={values.content_md ?? ""} onChange={onChange} />
    </EditPanel>
  );
}
