import { Upload } from "lucide-react";
import { useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useSubmit } from "../../../shared/hooks/useForm";
import { FormError } from "../../../shared/ui/Field";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

const BASE = "/admin/media/files";

export function MediaPage() {
  const list = useApi(`${BASE}/?page_size=500`);
  return (
    <>
      <div className={styles.toolbar}>
        <h1>Media library</h1>
        <UploadForm onDone={list.reload} />
      </div>
      <div className={styles.mediaGrid}>
        {(list.data?.results ?? []).map((file) => (
          <MediaCard key={file.id} file={file} onChange={list.reload} />
        ))}
      </div>
    </>
  );
}

function UploadForm({ onDone }) {
  const [file, setFile] = useState(null);
  const [alt, setAlt] = useState("");
  const { submit, busy, error } = useSubmit(async () => {
    const body = new FormData();
    body.append("file", file);
    body.append("alt_text", alt);
    await api(`${BASE}/`, { method: "POST", body });
    setAlt("");
    onDone();
  });
  return (
    <form onSubmit={submit} className={styles.actions}>
      <input type="file" accept=".jpg,.jpeg,.png,.gif,.webp,.pdf,.mp4" required onChange={(e) => setFile(e.target.files[0])} />
      <input placeholder="Alt text" value={alt} onChange={(e) => setAlt(e.target.value)} />
      <button className="btn btn-primary" disabled={busy}>
        <Upload /> {busy ? "Uploading…" : "Upload"}
      </button>
      <FormError error={error} />
    </form>
  );
}

function MediaCard({ file, onChange }) {
  async function saveAlt(alt_text) {
    if (alt_text !== file.alt_text) await api(`${BASE}/${file.id}/`, { method: "PATCH", body: { alt_text } });
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
      <RecordActions base={BASE} row={file} onChange={onChange} />
    </article>
  );
}
