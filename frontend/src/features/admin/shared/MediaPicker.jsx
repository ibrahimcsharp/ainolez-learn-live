import { Upload } from "lucide-react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useSubmit } from "../../../shared/hooks/useForm";
import { FormError } from "../../../shared/ui/Field";
import { MEDIA, uploadBody } from "../media/MediaPage";
import styles from "./admin.module.css";

/** Pick an image from the media library, or upload a new one right here. */
export function MediaPicker({ name, label, value, onChange }) {
  const list = useApi(`${MEDIA}/?page_size=500&active=1`);
  const images = useImages(list);
  const selected = images.find((file) => String(file.id) === String(value));
  const choose = (id) => onChange({ target: { name, value: id } });
  const upload = useSubmit(async (event) => {
    const saved = await api(`${MEDIA}/`, { method: "POST", body: uploadBody(event.target.files[0]) });
    list.reload();
    choose(saved.id);
  });

  return (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <div className={styles.picker}>
        {selected && <img src={selected.url} alt="" />}
        <select id={name} name={name} value={value ?? ""} onChange={onChange}>
          <option value="">— none —</option>
          {images.map((file) => (
            <option key={file.id} value={file.id}>
              {file.original_name}
              {file.alt_text && ` (${file.alt_text})`}
            </option>
          ))}
        </select>
        <label className={`btn btn-outline ${styles.small}`}>
          <Upload /> {upload.busy ? "Uploading…" : "Upload new"}
          <input type="file" accept="image/*" hidden onChange={upload.submit} />
        </label>
      </div>
      <FormError error={upload.error} />
    </div>
  );
}

export function useImages(list) {
  return (list.data?.results ?? []).filter((file) => file.mime_type.startsWith("image/"));
}
