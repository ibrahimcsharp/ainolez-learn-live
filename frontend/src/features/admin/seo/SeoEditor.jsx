import { RotateCcw, Save } from "lucide-react";
import { useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useFormFields, useSubmit } from "../../../shared/hooks/useForm";
import { Field, FormError } from "../../../shared/ui/Field";
import styles from "../shared/admin.module.css";
import seo from "./Seo.module.css";

export const SEO = "/admin/seo";
const BLANK = {
  meta_title: "", meta_description: "", keywords: "", canonical_url: "", robots: "",
  og_title: "", og_description: "", og_image_url: "", og_type: "", twitter_card: "",
  structured_data: "", in_sitemap: true, sitemap_priority: "", sitemap_changefreq: "",
};
const NULLABLE = ["robots", "twitter_card", "sitemap_priority", "sitemap_changefreq"];

/**
 * Every SEO setting of one page, found by its URL path. Empty fields stay
 * automatic; the hints show what the page gets then. Used on the SEO screen
 * and inside the course and lesson editors.
 */
export function SeoEditor({ path, onSaved }) {
  const lookup = useApi(`${SEO}/lookup/?path=${encodeURIComponent(path)}`);
  if (!lookup.data) return <p className="page-loading">{lookup.error?.message ?? "Loading…"}</p>;
  const { page, automatic, result } = lookup.data;
  const done = () => {
    lookup.reload();
    onSaved?.();
  };
  return (
    <SeoForm key={page?.updated_at ?? "new"} path={lookup.data.path} page={page}
      automatic={automatic} result={result} onSaved={done} />
  );
}

function SeoForm({ path, page, automatic, result, onSaved }) {
  const initial = { ...BLANK, ...fromPage(page) };
  const [values, onChange, setValues] = useFormFields(initial);
  const [jsonError, setJsonError] = useState("");
  const { submit, busy, error } = useSubmit(async () => {
    const body = toBody(values, path);
    await api(page ? `${SEO}/pages/${page.id}/` : `${SEO}/pages/`, { method: page ? "PATCH" : "POST", body });
    onSaved();
  });

  async function reset() {
    if (!confirm("Remove the custom settings? The page goes back to automatic values.")) return;
    await api(`${SEO}/pages/${page.id}/soft-delete/`, { method: "POST" });
    onSaved();
  }

  function save(event) {
    event.preventDefault();
    try {
      if (values.structured_data.trim()) JSON.parse(values.structured_data);
      setJsonError("");
      submit();
    } catch {
      setJsonError("Structured data is not valid JSON.");
    }
  }

  const field = (name, label, props = {}) => (
    <Field label={label} name={name} value={values[name]} onChange={onChange} error={error} {...props} />
  );
  const preview = {
    title: values.meta_title || automatic.title,
    description: values.meta_description || automatic.description,
    image: values.og_image_url || automatic.image,
    ogTitle: values.og_title || values.meta_title || automatic.og_title,
    ogDescription: values.og_description || values.meta_description || automatic.og_description,
  };

  return (
    <form className={`card ${styles.panel}`} onSubmit={save}>
      <div className={styles.toolbar}>
        <h3 style={{ margin: 0 }}>
          SEO of <code>{path}</code>
        </h3>
        <span className="muted">
          {result.status === 404 ? "Not public yet: tags apply once it is published. " : ""}
          {page ? (page.is_active ? "Custom settings" : "Custom settings (inactive)") : "Automatic"}
        </span>
      </div>
      <FormError error={error} />
      {jsonError && <p className="notice notice-error">{jsonError}</p>}

      <div className={seo.previews}>
        <div className={seo.google}>
          <span className={seo.gTitle}>{preview.title}</span>
          <span className={seo.gUrl}>{automatic.canonical}</span>
          <span>{preview.description}</span>
        </div>
        <div className={seo.social}>
          {preview.image ? <img src={preview.image} alt="" /> : <div className={seo.noImage}>No share image</div>}
          <strong>{preview.ogTitle}</strong>
          <span>{preview.ogDescription}</span>
        </div>
      </div>

      <h4>Search results</h4>
      <div className={styles.formGrid}>
        {field("meta_title", <Counted label="Title (used exactly as typed)" text={values.meta_title} max={60} />,
          { placeholder: automatic.title })}
        {field("keywords", "Keywords (comma separated)", { placeholder: automatic.keywords })}
        {field("canonical_url", "Canonical URL", { placeholder: automatic.canonical })}
        <Field label="Robots" name="robots" as="select" value={values.robots} onChange={onChange} error={error}>
          <option value="">Automatic ({automatic.robots})</option>
          {["index,follow", "noindex,follow", "index,nofollow", "noindex,nofollow"].map((r) => (
            <option key={r}>{r}</option>
          ))}
        </Field>
      </div>
      {field("meta_description", <Counted label="Description" text={values.meta_description} max={160} />,
        { as: "textarea", rows: 2, placeholder: automatic.description })}

      <h4>Social sharing (Open Graph, X / Twitter)</h4>
      <div className={styles.formGrid}>
        {field("og_title", "Share title", { placeholder: automatic.og_title })}
        <ImageField value={values.og_image_url} onChange={onChange} placeholder={automatic.image} />
        <Field label="Type" name="og_type" as="select" value={values.og_type} onChange={onChange} error={error}>
          <option value="">Automatic ({automatic.og_type})</option>
          {["website", "article", "profile", "video.other"].map((t) => <option key={t}>{t}</option>)}
        </Field>
        <Field label="X / Twitter card" name="twitter_card" as="select" value={values.twitter_card}
          onChange={onChange} error={error}>
          <option value="">Automatic ({automatic.twitter_card})</option>
          <option value="summary">summary</option>
          <option value="summary_large_image">summary_large_image</option>
        </Field>
      </div>
      {field("og_description", "Share description", { as: "textarea", rows: 2, placeholder: automatic.og_description })}

      <h4>Sitemap and structured data</h4>
      <div className={styles.formGrid}>
        <label className="field">
          <span>
            <input type="checkbox" checked={values.in_sitemap}
              onChange={(e) => setValues({ ...values, in_sitemap: e.target.checked })} /> List in sitemap.xml
          </span>
        </label>
        {field("sitemap_priority", "Priority (0.0 – 1.0)", { type: "number", min: 0, max: 1, step: 0.1 })}
        <Field label="Change frequency" name="sitemap_changefreq" as="select" value={values.sitemap_changefreq}
          onChange={onChange} error={error}>
          <option value="">Not set</option>
          {["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"].map((c) => <option key={c}>{c}</option>)}
        </Field>
      </div>
      <Field label="Extra JSON-LD (added to the automatic schema.org data)" name="structured_data" as="textarea"
        rows={4} className={styles.code} value={values.structured_data} onChange={onChange} error={error}
        placeholder='{"@context": "https://schema.org", "@type": "FAQPage", ...}' />
      {result.json_ld.length > 0 && (
        <details>
          <summary className="muted">Structured data on this page now ({result.json_ld.length})</summary>
          <pre className={styles.code}>{JSON.stringify(result.json_ld, null, 2)}</pre>
        </details>
      )}

      <div className={styles.actions} style={{ justifyContent: "flex-start" }}>
        <button className="btn btn-primary" disabled={busy}><Save /> {busy ? "Saving…" : "Save SEO"}</button>
        {page && (
          <button type="button" className={`btn btn-outline ${styles.danger}`} onClick={reset}>
            <RotateCcw /> Reset to automatic
          </button>
        )}
      </div>
    </form>
  );
}

function Counted({ label, text, max }) {
  const over = text.length > max;
  return (
    <>
      {label} <span className={over ? styles.danger : "muted"}>{text.length}/{max}</span>
    </>
  );
}

/** A share image: paste a URL or pick one from the media library. */
export function ImageField({ name = "og_image_url", label = "Share image (1200×630)", value, onChange, placeholder }) {
  const { data } = useApi("/admin/media/files/?page_size=500&active=1");
  const images = (data?.results ?? []).filter((file) => file.mime_type.startsWith("image/"));
  return (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <input id={name} name={name} value={value} onChange={onChange} placeholder={placeholder || "https://… or /media/…"}
        list={`${name}-library`} />
      <datalist id={`${name}-library`}>
        {images.map((file) => (
          <option key={file.id} value={file.url}>{file.original_name}</option>
        ))}
      </datalist>
    </div>
  );
}

function fromPage(page) {
  if (!page) return {};
  const values = Object.fromEntries(Object.keys(BLANK).map((key) => [key, page[key] ?? BLANK[key]]));
  values.structured_data = page.structured_data ? JSON.stringify(page.structured_data, null, 2) : "";
  return values;
}

function toBody(values, path) {
  const body = { ...values, path };
  NULLABLE.forEach((key) => {
    if (body[key] === "") body[key] = null;
  });
  body.structured_data = values.structured_data.trim() ? JSON.parse(values.structured_data) : null;
  return body;
}
