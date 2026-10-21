import {
  Bold,
  Code,
  Heading2,
  Heading3,
  ImagePlus,
  Italic,
  Lightbulb,
  Link as LinkIcon,
  List,
  ListOrdered,
  Minus,
  Quote,
  SquarePlay,
  Table,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { markdownFor, MEDIA, uploadBody } from "../media/MediaPage";
import { useImages } from "./MediaPicker";
import { useMarkdownPreview } from "./useMarkdownPreview";
import styles from "./MarkdownEditor.module.css";
import admin from "./admin.module.css";

/*
 * Each tool changes the selected text (or the current line) of the textarea.
 * `wrap` puts text around the selection, `line` adds a prefix to each selected
 * line, `block` inserts a block on its own lines.
 */
const TOOLS = [
  { icon: Heading2, label: "Heading", line: "## " },
  { icon: Heading3, label: "Small heading", line: "### " },
  { icon: Bold, label: "Bold (Ctrl+B)", wrap: ["**", "**", "bold text"], key: "b" },
  { icon: Italic, label: "Italic (Ctrl+I)", wrap: ["_", "_", "italic text"], key: "i" },
  { icon: LinkIcon, label: "Link (Ctrl+K)", link: true, key: "k" },
  "|",
  { icon: List, label: "Bulleted list", line: "- " },
  { icon: ListOrdered, label: "Numbered list", line: "1. " },
  { icon: Quote, label: "Quote", line: "> " },
  "|",
  { icon: Code, label: "Code block", block: (text) => "```python\n" + (text || "print(\"Hello\")") + "\n```" },
  { icon: Lightbulb, label: "Note box", callout: true },
  { icon: Table, label: "Table", block: () => "| Column | Column |\n| --- | --- |\n| Text | Text |" },
  { icon: SquarePlay, label: "Video (YouTube, Vimeo, .mp4)", block: () => "{{video:https://www.youtube.com/watch?v=}}" },
  { icon: Minus, label: "Divider", block: () => "---" },
];
const CALLOUTS = ["note", "tip", "warning", "example"];

/**
 * The smart editor: a Markdown text box with a formatting toolbar, image
 * upload (button, paste or drop: files go to the media library, so it works
 * before the page is saved) and a live preview rendered by the server, the
 * same sanitised HTML the public page shows.
 */
export function MarkdownEditor({ name, label, value, onChange, rows = 18 }) {
  const area = useRef(null);
  const latest = useRef(value);
  latest.current = value;
  const [selection, setSelection] = useState(null);
  const [uploading, setUploading] = useState(0);
  const [uploadError, setUploadError] = useState("");
  const [callout, setCallout] = useState(false);
  const html = useMarkdownPreview(value);
  const media = useApi(`${MEDIA}/?page_size=500&active=1`);
  const images = useImages(media);

  // Put the cursor back after a tool changed the text.
  useEffect(() => {
    if (!selection || !area.current) return;
    area.current.focus();
    area.current.setSelectionRange(selection[0], selection[1]);
  }, [selection]);

  function set(text, start, end = start) {
    onChange({ target: { name, value: text } });
    setSelection([start, end]);
  }

  function apply(tool) {
    const el = area.current;
    const [start, end] = [el.selectionStart, el.selectionEnd];
    const text = latest.current;
    const picked = text.slice(start, end);
    if (tool.wrap) {
      const [before, after, sample] = tool.wrap;
      const inner = picked || sample;
      set(text.slice(0, start) + before + inner + after + text.slice(end), start + before.length,
        start + before.length + inner.length);
    } else if (tool.link) {
      const inner = picked || "link text";
      const url = "https://";
      const next = `${text.slice(0, start)}[${inner}](${url})${text.slice(end)}`;
      const urlStart = start + inner.length + 3;
      set(next, urlStart, urlStart + url.length); // type the address straight away
    } else if (tool.line) {
      const lineStart = text.lastIndexOf("\n", start - 1) + 1;
      const found = text.indexOf("\n", Math.max(end - (end > start ? 1 : 0), start));
      const lineEnd = found === -1 ? text.length : found;
      const lines = text.slice(lineStart, lineEnd).split("\n");
      const changed = lines
        .map((line, i) => {
          const bare = line.replace(/^(#{1,6} |- |\d+\. |> )/, "");
          const prefix = tool.line === "1. " ? `${i + 1}. ` : tool.line;
          return line.startsWith(prefix) ? bare : prefix + bare; // pressing again removes it
        })
        .join("\n");
      set(text.slice(0, lineStart) + changed + text.slice(lineEnd), lineStart + changed.length);
    } else if (tool.block) {
      insertBlock(tool.block(picked), start, end);
    }
  }

  function insertBlock(block, start = area.current?.selectionStart ?? latest.current.length, end = start) {
    const text = latest.current;
    const before = text.slice(0, start).replace(/\s*$/, "");
    const after = text.slice(end).replace(/^\s*/, "");
    const head = before ? `${before}\n\n` : "";
    const next = head + block + (after ? `\n\n${after}` : "\n");
    set(next, head.length + block.length);
  }

  function addCallout(kind) {
    setCallout(false);
    const el = area.current;
    const picked = latest.current.slice(el.selectionStart, el.selectionEnd) || "Write the note here.";
    const body = picked.split("\n").map((line) => `    ${line}`).join("\n");
    insertBlock(`!!! ${kind}\n${body}`, el.selectionStart, el.selectionEnd);
  }

  async function upload(files) {
    const list = [...files].filter((file) => file.type.startsWith("image/"));
    if (!list.length) return;
    setUploadError("");
    setUploading((n) => n + list.length);
    for (const file of list) {
      try {
        const saved = await api(`${MEDIA}/`, { method: "POST", body: uploadBody(file, altFrom(file.name)) });
        insertBlock(markdownFor(saved));
      } catch (err) {
        setUploadError(`${file.name}: ${err.message}`);
      } finally {
        setUploading((n) => n - 1);
      }
    }
    media.reload();
  }

  function onKeyDown(event) {
    if (!(event.ctrlKey || event.metaKey)) return;
    const tool = TOOLS.find((t) => t.key === event.key.toLowerCase());
    if (tool) {
      event.preventDefault();
      apply(tool);
    }
  }

  return (
    <div className={styles.editor}>
      <label htmlFor={name} className={styles.label}>{label}</label>
      <div className={styles.toolbar} role="toolbar" aria-label="Formatting">
        {TOOLS.map((tool, i) =>
          tool === "|" ? (
            <span key={i} className={styles.sep} />
          ) : (
            <button key={tool.label} type="button" title={tool.label} aria-label={tool.label}
              onMouseDown={(e) => e.preventDefault()} // keep the text selection
              onClick={() => (tool.callout ? setCallout(!callout) : apply(tool))}>
              <tool.icon size={17} />
            </button>
          ),
        )}
        <span className={styles.sep} />
        <label className={styles.upload} title="Upload an image (or paste / drop one into the text)">
          <ImagePlus size={17} /> {uploading ? "Uploading…" : "Image"}
          <input type="file" accept="image/*" multiple hidden
            onChange={(e) => { upload(e.target.files); e.target.value = ""; }} />
        </label>
        <select aria-label="Insert an image from Media" value="" className={styles.library}
          onChange={(e) => insertBlock(markdownFor(images.find((f) => String(f.id) === e.target.value)))}>
          <option value="">From Media…</option>
          {images.map((file) => (
            <option key={file.id} value={file.id}>{file.original_name}</option>
          ))}
        </select>
      </div>
      {callout && (
        <div className={styles.callouts}>
          Note box kind:
          {CALLOUTS.map((kind) => (
            <button key={kind} type="button" className={`btn btn-outline ${admin.small}`}
              onMouseDown={(e) => e.preventDefault()} onClick={() => addCallout(kind)}>
              {kind}
            </button>
          ))}
        </div>
      )}
      {uploadError && <p className="notice notice-error">{uploadError}</p>}
      <div className={admin.split}>
        <textarea ref={area} id={name} name={name} rows={rows} value={value} onChange={onChange}
          onKeyDown={onKeyDown} className={`${admin.code} ${styles.text}`}
          placeholder="Write here. Use the buttons above, or Markdown: ## heading, **bold**, - list. Paste or drop images."
          onPaste={(e) => { if (e.clipboardData.files.length) { e.preventDefault(); upload(e.clipboardData.files); } }}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => { if (e.dataTransfer.files.length) { e.preventDefault(); upload(e.dataTransfer.files); } }} />
        <div>
          <span className={styles.previewLabel}>Preview</span>
          <div className={`lesson-content ${admin.preview} ${styles.preview}`} aria-live="polite"
            dangerouslySetInnerHTML={{ __html: html }} />
        </div>
      </div>
    </div>
  );
}

/** "team-photo_2.png" -> "team photo 2" */
function altFrom(fileName) {
  return fileName.replace(/\.[^.]+$/, "").replace(/[-_]+/g, " ").trim();
}
