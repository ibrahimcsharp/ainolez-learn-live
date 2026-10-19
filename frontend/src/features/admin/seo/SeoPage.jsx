import { useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useFormFields, useSubmit } from "../../../shared/hooks/useForm";
import { Field, FormError } from "../../../shared/ui/Field";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";
import { ImageField, SEO, SeoEditor } from "./SeoEditor";
import seo from "./Seo.module.css";

/** Admin -> SEO: site-wide defaults, any page's tags, and a report of problems. */
export function SeoPage() {
  const [tab, setTab] = useState("pages");
  const [editing, setEditing] = useState(null); // a URL path
  const open = (path) => {
    setEditing(path);
    setTab("pages");
    window.scrollTo({ top: 0 });
  };
  const tabs = {
    pages: ["Pages", <PagesTab key="pages" editing={editing} onOpen={open} onClose={() => setEditing(null)} />],
    site: ["Site defaults", <SiteTab key="site" />],
    report: ["SEO report and sitemap", <ReportTab key="report" onOpen={open} />],
  };
  return (
    <>
      <h1>SEO</h1>
      <p className="muted">
        Every public page gets its title, description, robots, canonical link, Open Graph, X / Twitter tags and
        schema.org data from here. Empty fields are automatic (from the course, lesson or post).
      </p>
      <div className={styles.tabs}>
        {Object.entries(tabs).map(([key, [label]]) => (
          <button key={key} className={`btn btn-outline ${styles.small}`} aria-pressed={tab === key}
            onClick={() => setTab(key)}>
            {label}
          </button>
        ))}
      </div>
      {tabs[tab][1]}
    </>
  );
}

function PagesTab({ editing, onOpen, onClose }) {
  const [q, setQ] = useState("");
  const list = useApi(`${SEO}/pages/?page_size=500&q=${encodeURIComponent(q)}`);
  function openTyped(event) {
    event.preventDefault();
    const path = new FormData(event.currentTarget).get("path").trim();
    if (path) onOpen(path.startsWith("/") ? path : `/${path}`);
  }
  return (
    <>
      <form className={styles.toolbar} onSubmit={openTyped}>
        <input name="path" placeholder="/courses, /python, /python/lists, /community/posts/12" style={{ flex: 1 }}
          aria-label="Page path" />
        <button className="btn btn-primary">Edit SEO of this page</button>
      </form>
      {editing && (
        <>
          <button className={`btn btn-outline ${styles.small}`} onClick={onClose}>Close editor</button>
          <SeoEditor key={editing} path={editing} onSaved={list.reload} />
        </>
      )}

      <div className={styles.toolbar}>
        <h2 style={{ margin: 0 }}>Pages with custom settings</h2>
        <input type="search" placeholder="Search" value={q} onChange={(e) => setQ(e.target.value)} />
      </div>
      <table className={styles.table}>
        <thead>
          <tr><th>Page</th><th>Title</th><th>Robots</th><th>Status</th><th /></tr>
        </thead>
        <tbody>
          {(list.data?.results ?? []).map((row) => (
            <tr key={row.id}>
              <td>
                <code>{row.url || "(item deleted)"}</code>
                {row.entity_type && <span className="muted"> · {row.entity_type}</span>}
              </td>
              <td>{row.meta_title || <span className="muted">automatic</span>}</td>
              <td>{row.robots ?? <span className="muted">automatic</span>}</td>
              <td><StatusBadge row={row} /></td>
              <td>
                <RecordActions base={`${SEO}/pages`} row={row} onChange={list.reload}
                  onEdit={row.url ? () => onOpen(row.url) : undefined} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

function SiteTab() {
  const { data, reload } = useApi(`${SEO}/settings/`);
  if (!data) return <p className="page-loading">Loading…</p>;
  return <SiteForm key={data.updated_at} initial={data} onSaved={reload} />;
}

function SiteForm({ initial, onSaved }) {
  const [values, onChange, setValues] = useFormFields({
    ...initial,
    social_profiles: initial.social_profiles.join("\n"),
    robots_txt_extra: initial.robots_txt_extra ?? "",
  });
  const { submit, busy, error } = useSubmit(async () => {
    const { last_build_at, last_build_pages, updated_at, ...rest } = values;
    await api(`${SEO}/settings/`, {
      method: "PATCH",
      body: { ...rest, social_profiles: values.social_profiles.split("\n").map((p) => p.trim()).filter(Boolean) },
    });
    onSaved();
  });
  const field = (name, label, props = {}) => (
    <Field label={label} name={name} value={values[name]} onChange={onChange} error={error} {...props} />
  );
  return (
    <form className={`card ${styles.panel}`} onSubmit={submit}>
      <FormError error={error} />
      <label style={{ display: "block", marginBottom: 12 }}>
        <input type="checkbox" checked={values.allow_indexing}
          onChange={(e) => setValues({ ...values, allow_indexing: e.target.checked })} />{" "}
        <strong>Let search engines index the site</strong>{" "}
        <span className="muted">(turn off on staging: every page becomes noindex and robots.txt blocks all)</span>
      </label>
      <div className={styles.formGrid}>
        {field("site_name", "Site name")}
        {field("title_template", "Title template for automatic titles", { placeholder: "{title} · ainolez" })}
        {field("locale", "Locale (og:locale)", { placeholder: "en_US" })}
        {field("default_keywords", "Default keywords")}
        <ImageField name="default_image_url" label="Default share image (1200×630)" value={values.default_image_url}
          onChange={onChange} />
        <ImageField name="organization_logo_url" label="Logo for Google (square)" value={values.organization_logo_url}
          onChange={onChange} />
        {field("twitter_site", "X / Twitter account", { placeholder: "@ainolez" })}
        {field("facebook_app_id", "Facebook app ID")}
        {field("google_site_verification", "Google Search Console code")}
        {field("bing_site_verification", "Bing Webmaster code")}
      </div>
      {field("default_description", "Default description", { as: "textarea", rows: 2 })}
      {field("social_profiles", "Social profile links, one per line (schema.org sameAs)", { as: "textarea", rows: 3 })}
      {field("robots_txt_extra", "Extra robots.txt lines", { as: "textarea", rows: 3, className: styles.code })}
      <button className="btn btn-primary" disabled={busy}>{busy ? "Saving…" : "Save"}</button>
    </form>
  );
}

function ReportTab({ onOpen }) {
  const report = useApi(`${SEO}/report/`);
  const [onlyIssues, setOnlyIssues] = useState(true);
  const [build, setBuild] = useState("");
  async function rebuild() {
    setBuild("Building…");
    try {
      const { pages } = await api(`${SEO}/build/`, { method: "POST" });
      setBuild(`✓ Wrote ${pages} pages, sitemap.xml and robots.txt.`);
      report.reload();
    } catch (error) {
      setBuild(error.message);
    }
  }
  if (!report.data) return <p className="page-loading">{report.error?.message ?? "Loading…"}</p>;
  const { pages, last_build_at: builtAt, last_build_pages: built, robots_txt: robots } = report.data;
  const shown = onlyIssues ? pages.filter((page) => page.issues.length) : pages;
  return (
    <>
      <section className={`card ${styles.panel}`}>
        <h3>Prerendered pages and sitemap</h3>
        <p className="muted">
          Rebuilt automatically a minute after content or SEO changes, and every night.{" "}
          {builtAt ? `Last build: ${new Date(builtAt).toLocaleString()} (${built} pages).` : "Not built yet."}
        </p>
        <button className="btn btn-outline" onClick={rebuild}>Rebuild now</button> <span>{build}</span>
        <details>
          <summary className="muted">robots.txt</summary>
          <pre className={styles.code}>{robots}</pre>
        </details>
      </section>

      <div className={styles.toolbar}>
        <h2 style={{ margin: 0 }}>
          {pages.filter((page) => page.issues.length).length} of {pages.length} pages need attention
        </h2>
        <label>
          <input type="checkbox" checked={onlyIssues} onChange={(e) => setOnlyIssues(e.target.checked)} /> Only pages
          with issues
        </label>
      </div>
      <table className={styles.table}>
        <thead>
          <tr><th>Page</th><th>Title and description</th><th>Robots</th><th /></tr>
        </thead>
        <tbody>
          {shown.map((page) => (
            <tr key={page.path}>
              <td>
                <code>{page.path}</code>
                {page.customised && <div className="muted">custom</div>}
              </td>
              <td>
                <strong>{page.title}</strong>
                <div className="muted">{page.description}</div>
                {page.issues.length > 0 && (
                  <ul className={seo.issues}>{page.issues.map((issue) => <li key={issue}>{issue}</li>)}</ul>
                )}
              </td>
              <td>{page.robots}{page.in_sitemap && <div className="muted">in sitemap</div>}</td>
              <td>
                <button className={`btn btn-outline ${styles.small}`} onClick={() => onOpen(page.path)}>Edit</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
