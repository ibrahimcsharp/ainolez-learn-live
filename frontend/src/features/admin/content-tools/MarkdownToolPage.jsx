import { useState } from "react";
import { useMarkdownPreview } from "../shared/useMarkdownPreview";
import styles from "../shared/admin.module.css";

const SAMPLE = `## Hello ainolez

Write **Markdown** on the left and see the result on the right.

!!! tip
    Put a video on its own line with \`{{youtube:VIDEO_ID}}\`, \`{{vimeo:VIDEO_ID}}\`
    or \`{{video:https://example.com/clip.mp4}}\`.
`;

/** Paste Markdown, preview it, copy the safe HTML. Imports live on each chapter. */
export function MarkdownToolPage() {
  const [markdown, setMarkdown] = useState(SAMPLE);
  const html = useMarkdownPreview(markdown);
  return (
    <>
      <div className={styles.toolbar}>
        <h1>Markdown converter</h1>
        <button className="btn btn-outline" onClick={() => navigator.clipboard.writeText(html)}>
          Copy HTML
        </button>
      </div>
      <p className="muted">
        To turn .md files into lessons, open a course and use “Import Markdown” on a chapter.
      </p>
      <div className={styles.split}>
        <textarea className={`${styles.code} ${styles.preview}`} rows={24} value={markdown}
          onChange={(e) => setMarkdown(e.target.value)} aria-label="Markdown" />
        <div className={`lesson-content ${styles.preview}`} dangerouslySetInnerHTML={{ __html: html }} />
      </div>
    </>
  );
}
