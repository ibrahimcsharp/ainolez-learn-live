import { Plus } from "lucide-react";
import { useState } from "react";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { MediaPicker } from "../shared/MediaPicker";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import { SortableList } from "../shared/SortableList";
import { useMarkdownPreview } from "../shared/useMarkdownPreview";
import styles from "../shared/admin.module.css";

const BLOCKS = "/admin/catalog/blocks";
const TYPES = {
  markdown: "Text (Markdown)",
  example: "Code example",
  video: "Video",
  callout: "Callout box",
  image: "Image",
  embed: "Embed",
  exercise: "Exercise",
  quiz: "Quiz",
};
const LANGUAGE_OPTIONS = ["html", "css", "javascript", "python", "sql"].map((k) => <option key={k}>{k}</option>);
const VIDEO_PAGES = {
  youtube: (ref) => `https://www.youtube.com/watch?v=${ref}`,
  vimeo: (ref) => `https://vimeo.com/${ref}`,
  loom: (ref) => `https://www.loom.com/share/${ref}`,
  drive: (ref) => `https://drive.google.com/file/d/${ref}/view`,
  file: (ref) => ref,
};

/** The ordered blocks of one lesson: add, edit, reorder, hide and trash them. */
export function BlocksEditor({ lessonId, courseId, blocks, onChange }) {
  const [editingId, setEditingId] = useState(null);
  const [newType, setNewType] = useState(null);

  function saved() {
    setEditingId(null);
    setNewType(null);
    onChange();
  }

  return (
    <section>
      <h2>Blocks</h2>
      <SortableList
        items={blocks}
        base={BLOCKS}
        onChange={onChange}
        renderItem={(block) =>
          editingId === block.id ? (
            <BlockForm lessonId={lessonId} courseId={courseId} block={block} type={block.type}
              onSaved={saved} onCancel={() => setEditingId(null)} />
          ) : (
            <div className={styles.toolbar} style={{ margin: 0 }}>
              <span className={styles.grow}>
                <strong>{TYPES[block.type]}</strong> <StatusBadge row={block} />
                <div className="muted">{summary(block)}</div>
              </span>
              <RecordActions base={BLOCKS} row={block} onChange={onChange} onEdit={() => setEditingId(block.id)} />
            </div>
          )
        }
      />
      {newType && (
        <BlockForm lessonId={lessonId} courseId={courseId} type={newType} onSaved={saved}
          onCancel={() => setNewType(null)} />
      )}
      <div className={styles.actions} style={{ justifyContent: "flex-start", marginTop: 12 }}>
        {Object.entries(TYPES).map(([type, label]) => (
          <button key={type} className="btn btn-outline" onClick={() => setNewType(type)}>
            <Plus /> {label}
          </button>
        ))}
      </div>
    </section>
  );
}

function summary(block) {
  if (block.type === "example") return block.example?.starter_code.slice(0, 90);
  if (block.type === "video") return block.data?.caption || VIDEO_PAGES[block.data?.provider]?.(block.data.ref);
  if (block.type === "embed") return block.data?.url;
  if (block.type === "exercise") return block.exercise?.prompt_md.slice(0, 120);
  if (block.type === "quiz") return `Quiz #${block.quiz_id}`;
  return (block.content_md ?? "").slice(0, 120);
}

/** Fields for one block. The form keeps flat values and builds the API body per type. */
function BlockForm({ lessonId, courseId, block, type, onSaved, onCancel }) {
  const data = block?.data ?? {};
  const code = block?.example ?? block?.exercise ?? {}; // example and exercise share these fields
  const initial = {
    id: block?.id,
    content_md: block?.content_md ?? "",
    kind: data.kind ?? "note",
    url: data.url ?? (data.provider ? VIDEO_PAGES[data.provider](data.ref) : ""),
    start: data.start ?? 0,
    caption: data.caption ?? "",
    alt: data.alt ?? "",
    title: data.title ?? code.title ?? "",
    media_id: block?.media_id ?? "",
    language: code.language ?? "html",
    starter_code: code.starter_code ?? "",
    prompt_md: block?.exercise?.prompt_md ?? "",
    solution_code: block?.exercise?.solution_code ?? "",
    check_type: block?.exercise?.check_type ?? "output",
    expected_value: block?.exercise?.expected_value ?? "",
    hint: block?.exercise?.hint ?? "",
    quiz_id: block?.quiz_id ?? "",
  };
  const form = useResourceForm(BLOCKS, initial, onSaved, (v) => toBody(lessonId, type, v));
  const { values, onChange, error } = form;
  const field = (label, name, props = {}) => (
    <Field label={label} name={name} value={values[name]} onChange={onChange} error={error} {...props} />
  );

  return (
    <EditPanel title={`${block ? "Edit" : "New"} ${TYPES[type].toLowerCase()}`} form={form} onCancel={onCancel}>
      {type === "callout" &&
        field("Kind", "kind", {
          as: "select",
          children: ["note", "tip", "warning", "example"].map((k) => <option key={k}>{k}</option>),
        })}
      {(type === "markdown" || type === "callout") && <MarkdownField values={values} onChange={onChange} error={error} />}
      {type === "example" && (
        <>
          {field("Title (optional)", "title")}
          {field("Language", "language", { as: "select", children: LANGUAGE_OPTIONS })}
          <div style={{ gridColumn: "1 / -1" }}>
            {field("Code", "starter_code", { as: "textarea", rows: 8, className: styles.code, required: true })}
          </div>
        </>
      )}
      {type === "video" && (
        <>
          {field("Video link (YouTube, Vimeo, Loom, Google Drive or .mp4)", "url", { required: true })}
          {field("Start at (seconds)", "start", { type: "number", min: 0 })}
          {field("Caption", "caption")}
        </>
      )}
      {type === "image" && (
        <>
          <MediaPicker name="media_id" label="Image" value={values.media_id} onChange={onChange} />
          {field("Alt text (blank = from library)", "alt")}
          {field("Caption", "caption")}
        </>
      )}
      {type === "exercise" && (
        <>
          {field("Title (optional)", "title")}
          {field("Language", "language", { as: "select", children: LANGUAGE_OPTIONS })}
          <div style={{ gridColumn: "1 / -1" }}>
            {field("Task (Markdown)", "prompt_md", { as: "textarea", rows: 4, required: true })}
          </div>
          {field("Starter code", "starter_code", { as: "textarea", rows: 5, className: styles.code })}
          {field("Solution (for admins)", "solution_code", { as: "textarea", rows: 5, className: styles.code })}
          {field("How to check", "check_type", {
            as: "select",
            children: [
              <option key="output" value="output">What the code prints equals…</option>,
              <option key="contains" value="contains">The code contains…</option>,
              <option key="regex" value="regex">The code matches the regex…</option>,
              <option key="exact" value="exact">The code is exactly…</option>,
            ],
          })}
          {field("Expected answer", "expected_value", { as: "textarea", rows: 3, className: styles.code, required: true })}
          {field("Hint", "hint")}
        </>
      )}
      {type === "quiz" && <QuizPicker courseId={courseId} value={values.quiz_id} onChange={onChange} />}
      {type === "embed" && (
        <>
          {field("Embed link (CodePen, Replit, Google Slides…)", "url", { required: true })}
          {field("Title", "title")}
        </>
      )}
    </EditPanel>
  );
}

function MarkdownField({ values, onChange, error }) {
  const html = useMarkdownPreview(values.content_md);
  return (
    <div className={styles.split} style={{ gridColumn: "1 / -1" }}>
      <Field label="Markdown" name="content_md" as="textarea" rows={12} className={styles.code}
        value={values.content_md} onChange={onChange} error={error} />
      <div>
        <strong>Preview</strong>
        <div className={`lesson-content ${styles.preview}`} dangerouslySetInnerHTML={{ __html: html }} />
      </div>
    </div>
  );
}

function toBody(lesson, type, v) {
  const body = { lesson, type };
  if (type === "markdown") return { ...body, content_md: v.content_md };
  if (type === "callout") return { ...body, content_md: v.content_md, data: { kind: v.kind } };
  if (type === "example") {
    return { ...body, example: { title: v.title, language: v.language, starter_code: v.starter_code } };
  }
  if (type === "video") return { ...body, data: { url: v.url, start: Number(v.start) || 0, caption: v.caption } };
  if (type === "image") return { ...body, media_id: v.media_id || null, data: { alt: v.alt, caption: v.caption } };
  if (type === "exercise") {
    const exercise = Object.fromEntries(
      ["title", "language", "starter_code", "prompt_md", "solution_code", "check_type", "expected_value", "hint"]
        .map((key) => [key, v[key]]),
    );
    return { ...body, exercise };
  }
  if (type === "quiz") return { ...body, quiz_id: v.quiz_id || null };
  return { ...body, data: { url: v.url, title: v.title } }; // embed
}

function QuizPicker({ courseId, value, onChange }) {
  const { data } = useApi(`/admin/assessment/quizzes/?course_id=${courseId}&page_size=500`);
  return (
    <Field label="Quiz (build quizzes on the course page)" name="quiz_id" as="select" required value={value}
      onChange={onChange}>
      <option value="">Choose…</option>
      {(data?.results ?? []).map((quiz) => (
        <option key={quiz.id} value={quiz.id}>
          {quiz.title}
          {quiz.is_final && " (final)"}
        </option>
      ))}
    </Field>
  );
}
