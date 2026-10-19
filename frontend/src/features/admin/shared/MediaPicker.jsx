import { useApi } from "../../../shared/hooks/useApi";

/** A <select> of the images in the media library. */
export function MediaPicker({ name, label, value, onChange }) {
  const { data } = useApi("/admin/media/files/?page_size=500&active=1");
  const images = (data?.results ?? []).filter((file) => file.mime_type.startsWith("image/"));

  return (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <select id={name} name={name} value={value ?? ""} onChange={onChange}>
        <option value="">— none —</option>
        {images.map((file) => (
          <option key={file.id} value={file.id}>
            {file.original_name}
            {file.alt_text && ` (${file.alt_text})`}
          </option>
        ))}
      </select>
    </div>
  );
}
