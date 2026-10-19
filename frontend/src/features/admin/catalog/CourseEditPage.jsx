import { Plus, Save } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useSubmit } from "../../../shared/hooks/useForm";
import { Field, FormError } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { MediaPicker } from "../shared/MediaPicker";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import { SortableList } from "../shared/SortableList";
import styles from "../shared/admin.module.css";
import { QuizForm, QUIZZES } from "../assessment/QuizEditPage";
import { SeoEditor } from "../seo/SeoEditor";
import { CategorySelect, COURSES } from "./CoursesPage";

const CHAPTERS = "/admin/catalog/chapters";
const LESSONS = "/admin/catalog/lessons";

export function CourseEditPage() {
  const { id } = useParams();
  const course = useApi(`${COURSES}/${id}/`);
  if (!course.data) return <p className="page-loading">{course.error?.message ?? "Loading…"}</p>;

  return (
    <>
      <div className={styles.toolbar}>
        <h1>{course.data.title}</h1>
        <span>
          <StatusBadge row={course.data} />{" "}
          {course.data.ai_generated && <span className="muted">✨ AI generated · review before publishing </span>}
          {course.data.status === "published" && <a href={`/${course.data.slug}`}>View on site</a>}
        </span>
      </div>
      <CourseForm key={course.data.updated_at} initial={course.data} onSaved={course.reload} />
      <details className={styles.panel}>
        <summary><strong>SEO and social sharing</strong></summary>
        <SeoEditor key={course.data.slug} path={`/${course.data.slug}`} />
      </details>
      <Chapters courseId={id} />
      <Quizzes courseId={Number(id)} />
    </>
  );
}

function CourseForm({ initial, onSaved }) {
  const toBody = (v) => ({ ...v, thumbnail_media_id: v.thumbnail_media_id || null });
  const form = useResourceForm(COURSES, initial, onSaved, toBody);
  const { values, onChange, error } = form;
  return (
    <EditPanel title="Course details" form={form}>
      <Field label="Title" name="title" required value={values.title} onChange={onChange} error={error} />
      <Field label="Slug (URL)" name="slug" value={values.slug} onChange={onChange} error={error} />
      <CategorySelect value={values.category} onChange={onChange} error={error} />
      <Field label="Status" name="status" as="select" value={values.status} onChange={onChange} error={error}>
        <option value="draft">Draft</option>
        <option value="published">Published</option>
        <option value="archived">Archived</option>
      </Field>
      <Field label="Level" name="level" as="select" value={values.level} onChange={onChange} error={error}>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </Field>
      <Field label="Language" name="language_key" as="select" value={values.language_key} onChange={onChange} error={error}>
        {["html", "css", "javascript", "python", "sql", "ai", "other"].map((key) => (
          <option key={key} value={key}>
            {key}
          </option>
        ))}
      </Field>
      <Field label="Minutes to finish" name="estimated_minutes" type="number" min="0"
        value={values.estimated_minutes} onChange={onChange} error={error} />
      <MediaPicker name="thumbnail_media_id" label="Thumbnail" value={values.thumbnail_media_id} onChange={onChange} />
      <Field label="Short description" name="short_description" value={values.short_description}
        onChange={onChange} error={error} />
      <Field label="Description" name="description" as="textarea" rows={3} value={values.description ?? ""}
        onChange={onChange} error={error} />
    </EditPanel>
  );
}

function Chapters({ courseId }) {
  const chapters = useApi(`${CHAPTERS}/?course=${courseId}&page_size=500`);
  const lessons = useApi(`${LESSONS}/?course=${courseId}&page_size=500`);
  const reload = () => {
    chapters.reload();
    lessons.reload();
  };

  return (
    <section>
      <div className={styles.toolbar}>
        <h2>Chapters and lessons</h2>
        <QuickAdd placeholder="New chapter title" onAdd={(title) =>
          api(`${CHAPTERS}/`, { method: "POST", body: { course: courseId, title } }).then(reload)} />
      </div>
      <SortableList
        items={chapters.data?.results ?? []}
        base={CHAPTERS}
        onChange={reload}
        renderItem={(chapter) => (
          <Chapter
            chapter={chapter}
            lessons={(lessons.data?.results ?? []).filter((lesson) => lesson.chapter === chapter.id)}
            onChange={reload}
          />
        )}
      />
    </section>
  );
}

function Chapter({ chapter, lessons, onChange }) {
  const [renaming, setRenaming] = useState(false);
  return (
    <>
      <div className={styles.toolbar} style={{ marginBottom: 8 }}>
        {renaming ? (
          <QuickAdd initial={chapter.title} placeholder="Chapter title" onAdd={(title) =>
            api(`${CHAPTERS}/${chapter.id}/`, { method: "PATCH", body: { title } })
              .then(() => setRenaming(false)).then(onChange)} />
        ) : (
          <strong>
            {chapter.title} <StatusBadge row={chapter} />
          </strong>
        )}
        <RecordActions base={CHAPTERS} row={chapter} onChange={onChange} onEdit={() => setRenaming(true)} />
      </div>
      <SortableList
        items={lessons}
        base={LESSONS}
        onChange={onChange}
        renderItem={(lesson) => (
          <div className={styles.toolbar} style={{ margin: 0 }}>
            <span>
              <Link to={`/admin/lessons/${lesson.id}`}>{lesson.title}</Link> <StatusBadge row={lesson} />
              {lesson.ai_generated && <span className="muted"> ✨ AI draft</span>}
            </span>
            <RecordActions base={LESSONS} row={lesson} onChange={onChange} />
          </div>
        )}
      />
      <div className={styles.toolbar} style={{ marginTop: 8 }}>
        <QuickAdd placeholder="New lesson title" onAdd={(title) =>
          api(`${LESSONS}/`, { method: "POST", body: { chapter: chapter.id, title } }).then(onChange)} />
        <MarkdownImport chapterId={chapter.id} onDone={onChange} />
      </div>
    </>
  );
}

/** One text box + Add button. */
function QuickAdd({ placeholder, onAdd, initial = "" }) {
  const [text, setText] = useState(initial);
  const { submit, busy, error } = useSubmit(async () => {
    await onAdd(text);
    setText("");
  });
  return (
    <form onSubmit={submit} className={styles.actions}>
      <input value={text} onChange={(e) => setText(e.target.value)} placeholder={placeholder} required />
      <button className={`btn btn-outline ${styles.small}`} disabled={busy}>
        <Save /> Save
      </button>
      {error && <span className="field-error">{error.message}</span>}
    </form>
  );
}

/** Upload .md files or a .zip; each file becomes a lesson in this chapter. */
function MarkdownImport({ chapterId, onDone }) {
  const [files, setFiles] = useState([]);
  const [publish, setPublish] = useState(false);
  const { submit, busy, error } = useSubmit(async () => {
    const body = new FormData();
    body.append("chapter", chapterId);
    body.append("publish", publish ? "1" : "0");
    [...files].forEach((file) => body.append("files", file));
    await api(`${LESSONS}/import/`, { method: "POST", body });
    setFiles([]);
    onDone();
  });

  return (
    <form onSubmit={submit} className={styles.actions}>
      <input type="file" accept=".md,.zip" multiple onChange={(e) => setFiles(e.target.files)} />
      <label>
        <input type="checkbox" checked={publish} onChange={(e) => setPublish(e.target.checked)} /> Publish now
      </label>
      <button className={`btn btn-primary ${styles.small}`} disabled={busy || !files.length}>
        {busy ? "Importing…" : "Import Markdown"}
      </button>
      <FormError error={error} />
    </form>
  );
}

/** The course's quizzes. Put one in a lesson with a quiz block. */
function Quizzes({ courseId }) {
  const list = useApi(`${QUIZZES}/?course_id=${courseId}&page_size=500`);
  const [creating, setCreating] = useState(false);
  const navigate = useNavigate();
  const blank = { course_id: courseId, title: "", description: "", is_final: false, pass_percentage: 70 };

  return (
    <section style={{ marginTop: 32 }}>
      <div className={styles.toolbar}>
        <h2>Quizzes</h2>
        <button className="btn btn-primary" onClick={() => setCreating(true)}>
          <Plus /> New quiz
        </button>
      </div>
      {creating && (
        <QuizForm initial={blank} onSaved={(quiz) => navigate(`/admin/quizzes/${quiz.id}`)}
          onCancel={() => setCreating(false)} />
      )}
      <table className={styles.table}>
        <tbody>
          {(list.data?.results ?? []).map((quiz) => (
            <tr key={quiz.id}>
              <td>
                <Link to={`/admin/quizzes/${quiz.id}`}>{quiz.title}</Link> {quiz.is_final && <strong>(final)</strong>}{" "}
                <StatusBadge row={quiz} />
              </td>
              <td>
                <RecordActions base={QUIZZES} row={quiz} onChange={list.reload}
                  onEdit={() => navigate(`/admin/quizzes/${quiz.id}`)} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
