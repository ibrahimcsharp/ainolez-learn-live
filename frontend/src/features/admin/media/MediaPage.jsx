import { Check, Copy, FileText, Image, Link as LinkIcon, Upload } from "lucide-react";
import { useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useSubmit } from "../../../shared/hooks/useForm";
import { FormError } from "../../../shared/ui/Field";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

export const MEDIA = "/admin/media/files";

export function MediaPage() {
  const list = useApi(`${MEDIA}/?page_size=500`);
  return (
    <>
      <div className={styles.toolbar}>
        <h1>Media library</h1>
        <UploadForm onDone={list.reload} />
      </div>
      <section className={`card ${styles.panel}`}>
        <h3>How to use your files</h3>
        <ul className={styles.howTo}>
          <li>
            <Image /> <span><strong>In a lesson:</strong> open the lesson, add an <em>Image</em> block and pick the
            file. In a <em>Text</em> block, use <em>Add an image from Media</em> above the text box.</span>
          </li>
          <li>
            <FileText /> <span><strong>As a course picture:</strong> open the course, then <em>Details</em> →
            Thumbnail.</span>
          </li>
          <li>
            <LinkIcon /> <span><strong>Anywhere else:</strong> press <em>Copy link</em> (or <em>Copy Markdown</em>)
            on a file below and paste it into any text. PDFs become a download link, .mp4 files can go in a
            Video block.</span>
          </li>
        </ul>
      </section>
      <div className={styles.mediaGrid}>
        {(list.data?.results ?? []).map((file) => (
          <MediaCard key={file.id} file={file} onChange={list.reload} />
        ))}
      </div>
    </>
  );
}

/** Upload one file. `onDone(file)` gets the saved file. */
export function UploadForm({ onDone, accept = ".jpg,.jpeg,.png,.gif,.webp,.pdf,.mp4" }) {
  const [file, setFile] = useState(null);
  const [alt, setAlt] = useState("");
  const { submit, busy, error } = useSubmit(async () => {
    const saved = await api(`${MEDIA}/`, { method: "POST", body: uploadBody(file, alt) });
    setAlt("");
    onDone(saved);
  });
  return (
    <form onSubmit={submit} className={styles.actions}>
      <input type="file" accept={accept} required onChange={(e) => setFile(e.target.files[0])} />
      <input placeholder="Alt text (describe the image)" value={alt} onChange={(e) => setAlt(e.target.value)} />
      <button className="btn btn-primary" disabled={busy}>
        <Upload /> {busy ? "Uploading…" : "Upload"}
      </button>
      <FormError error={error} />
    </form>
  );
}

export function uploadBody(file, alt = "") {
  const body = new FormData();
  body.append("file", file);
  body.append("alt_text", alt);
  return body;
}

/** `![alt](url)` for images, `[name](url)` for other files. */
export function markdownFor(file) {
  const text = file.alt_text || file.original_name;
  return file.mime_type.startsWith("image/") ? `![${text}](${file.url})` : `[${text}](${file.url})`;
}

function MediaCard({ file, onChange }) {
  async function saveAlt(alt_text) {
    if (alt_text !== file.alt_text) await api(`${MEDIA}/${file.id}/`, { method: "PATCH", body: { alt_text } });
  }
  return (
    <article className="card" style={{ padding: 12 }}>
      {file.mime_type.startsWith("image/") ? (
        <img className={styles.mediaThumb} src={file.url} alt={file.alt_text} />
      ) : (
        <div className={styles.mediaThumb}>{file.mime_type}</div>
      )}
      <p style={{ margin: "8px 0 4px", wordBreak: "break-all" }}>
        <a href={file.url} target="_blank" rel="noreferrer">{file.original_name}</a> <StatusBadge row={file} />
      </p>
      <p className="muted" style={{ margin: 0 }}>
        {Math.ceil(file.size_bytes / 1024)} KB{file.width && ` · ${file.width}×${file.height}`}
      </p>
      <input defaultValue={file.alt_text} placeholder="Alt text" aria-label="Alt text"
        onBlur={(e) => saveAlt(e.target.value)} style={{ width: "100%", margin: "8px 0" }} />
      <div className={styles.actions} style={{ justifyContent: "flex-start", marginBottom: 8 }}>
        <CopyButton text={file.url} label="Copy link" />
        <CopyButton text={markdownFor(file)} label="Copy Markdown" />
      </div>
      <RecordActions base={MEDIA} row={file} onChange={onChange} />
    </article>
  );
}

function CopyButton({ text, label }) {
  const [copied, setCopied] = useState(false);
  async function copy() {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }
  return (
    <button type="button" className={`btn btn-outline ${styles.small}`} onClick={copy}>
      {copied ? <><Check /> Copied</> : <><Copy /> {label}</>}
    </button>
  );
}
