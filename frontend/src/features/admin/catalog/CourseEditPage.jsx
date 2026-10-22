import { ArrowLeft, Clock, ExternalLink, FileUp, Plus, Rocket, Undo2 } from "lucide-react";
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
import { CategorySelect, COURSES, LANGUAGES } from "./CoursesPage";

const CHAPTERS = "/admin/catalog/chapters";
const LESSONS = "/admin/catalog/lessons";
const TABS = { lessons: "Lessons", details: "Details", quizzes: "Quizzes", seo: "SEO" };

export function CourseEditPage() {
  const { id } = useParams();
  const course = useApi(`${COURSES}/${id}/`);
  const [tab, setTab] = useState("lessons");
  if (!course.data) return <p className={course.error ? "page-loading" : "page-loading is-loading"}>{course.error?.message ?? "Loading…"}</p>;
  const { data } = course;

  return (
    <>
      <Link to="/admin/courses" className={styles.back}>
        <ArrowLeft size={16} /> All courses
      </Link>
      <div className={styles.toolbar}>
        <div>
          <h1>{data.title}</h1>
          <span className="muted">/{data.slug}</span> <StatusBadge row={data} />
          {data.ai_generated && <span className="muted"> ✨ AI generated · review before publishing</span>}
        </div>
        <div className={styles.actions}>
          {data.status === "published" && (
            <a className="btn btn-outline" href={`/${data.slug}`}>
              <ExternalLink /> View on site
            </a>
          )}
          <PublishButton course={data} onDone={course.reload} />
        </div>
      </div>
      <div className={styles.tabs} role="tablist">
        {Object.entries(TABS).map(([key, label]) => (
          <button key={key} role="tab" className={`btn btn-outline ${styles.small}`} aria-pressed={tab === key}
            onClick={() => setTab(key)}>
            {label}
          </button>
        ))}
      </div>
      {tab === "lessons" && <Chapters courseId={Number(id)} />}
      {tab === "details" && <CourseForm key={data.updated_at} initial={data} onSaved={course.reload} />}
      {tab === "quizzes" && <Quizzes courseId={Number(id)} />}
      {tab === "seo" && (
        <section className="card">
          <SeoEditor key={data.slug} path={`/${data.slug}`} />
        </section>
      )}
    </>
  );
}

/** Publishing puts the course and all its draft lessons live; unpublishing hides the course only. */
function PublishButton({ course, onDone }) {
  const [message, setMessage] = useState("");
  const live = course.status === "published";
  const { submit, busy, error } = useSubmit(async () => {
    if (live) {
      await api(`${COURSES}/${course.id}/`, { method: "PATCH", body: { status: "draft" } });
      setMessage("");
    } else {
      const { lessons_published: count } = await api(`${COURSES}/${course.id}/publish/`, { method: "POST" });
      setMessage(count ? `Published with ${count} lesson${count === 1 ? "" : "s"}.` : "Published.");
    }
    onDone();
  });
  return (
    <>
      {message && <span className="muted">{message}</span>}
      {error && <span className={styles.danger}>{error.message}</span>}
      <button className={live ? "btn btn-outline" : "btn btn-primary"} disabled={busy} onClick={submit}>
        {live ? <><Undo2 /> Unpublish</> : <><Rocket /> Publish course</>}
      </button>
    </>
  );
}

function CourseForm({ initial, onSaved }) {
  const toBody = (v) => ({ ...v, thumbnail_media_id: v.thumbnail_media_id || null });
  const form = useResourceForm(COURSES, initial, onSaved, toBody);
  const { values, onChange, error } = form;
  return (
    <EditPanel form={form}>
      <Field label="Title" name="title" required value={values.title} onChange={onChange} error={error} />
      <Field label="Web address (/slug)" name="slug" value={values.slug} onChange={onChange} error={error} />
      <CategorySelect value={values.category} onChange={onChange} error={error} />
      <Field label="Level" name="level" as="select" value={values.level} onChange={onChange} error={error}>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </Field>
      <Field label="Code language" name="language_key" as="select" value={values.language_key} onChange={onChange}
        error={error}>
        {LANGUAGES}
      </Field>
      <Field label="Minutes to finish" name="estimated_minutes" type="number" min="0"
        value={values.estimated_minutes} onChange={onChange} error={error} />
      <MediaPicker name="thumbnail_media_id" label="Thumbnail" value={values.thumbnail_media_id} onChange={onChange} />
      <Field label="Intro video (YouTube link, optional)" name="intro_video_url" value={values.intro_video_url}
        onChange={onChange} error={error} placeholder="https://www.youtube.com/watch?v=…" />
      <div style={{ gridColumn: "1 / -1" }}>
        <Field label="Short description (on course cards)" name="short_description" value={values.short_description}
          onChange={onChange} error={error} />
        <Field label="Description (on the course page)" name="description" as="textarea" rows={3}
          value={values.description ?? ""} onChange={onChange} error={error} />
      </div>
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
  const addChapter = (title) => api(`${CHAPTERS}/`, { method: "POST", body: { course: courseId, title } }).then(reload);
  if (!chapters.data) return <p className="page-loading is-loading">Loading…</p>;

  if (!chapters.data.results.length) {
    return (
      <section className={`card ${styles.empty}`}>
        <h3>Add your first chapter</h3>
        <p className="muted">
          A course is made of chapters, and each chapter holds lessons. Name the first chapter, for example
          “Getting started”, then add lessons to it.
        </p>
        <QuickAdd placeholder="Chapter name" label="Add chapter" onAdd={addChapter} />
      </section>
    );
  }

  return (
    <section>
      <SortableList
        items={chapters.data.results}
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
      <div className={styles.addRow}>
        <QuickAdd placeholder="New chapter name" label="Add chapter" onAdd={addChapter} />
      </div>
    </section>
  );
}

function Chapter({ chapter, lessons, onChange }) {
  const [renaming, setRenaming] = useState(false);
  const [importing, setImporting] = useState(false);
  const navigate = useNavigate();
  const addLesson = (title) =>
    api(`${LESSONS}/`, { method: "POST", body: { chapter: chapter.id, title } })
      .then((lesson) => navigate(`/admin/lessons/${lesson.id}`));

  return (
    <div className={styles.grow}>
      <div className={styles.toolbar} style={{ marginBottom: 8 }}>
        {renaming ? (
          <QuickAdd initial={chapter.title} placeholder="Chapter name" label="Save" onAdd={(title) =>
            api(`${CHAPTERS}/${chapter.id}/`, { method: "PATCH", body: { title } })
              .then(() => setRenaming(false)).then(onChange)} />
        ) : (
          <strong className={styles.chapterTitle}>
            {chapter.title} <StatusBadge row={chapter} />
          </strong>
        )}
        <RecordActions base={CHAPTERS} row={chapter} onChange={onChange} onEdit={() => setRenaming(true)} />
      </div>
      {lessons.length ? (
        <SortableList
          items={lessons}
          base={LESSONS}
          onChange={onChange}
          renderItem={(lesson) => (
            <div className={styles.toolbar} style={{ margin: 0 }}>
              <span className={styles.grow}>
                <Link to={`/admin/lessons/${lesson.id}`}>{lesson.title}</Link> <StatusBadge row={lesson} />
                {lesson.ai_generated && <span className="muted"> ✨ AI draft</span>}
                <span className="muted"> · <Clock size={13} /> {lesson.estimated_minutes} min</span>
              </span>
              <RecordActions base={LESSONS} row={lesson} onChange={onChange} />
            </div>
          )}
        />
      ) : (
        <p className="muted">No lessons in this chapter yet.</p>
      )}
      <div className={styles.addRow}>
        <QuickAdd placeholder="New lesson title" label="Add lesson" onAdd={addLesson} />
        <button type="button" className={`btn btn-outline ${styles.small}`} aria-pressed={importing}
          onClick={() => setImporting(!importing)}>
          <FileUp /> Import .md files
        </button>
      </div>
      {importing && <MarkdownImport chapterId={chapter.id} onDone={() => { setImporting(false); onChange(); }} />}
    </div>
  );
}

/** One text box and a button. */
function QuickAdd({ placeholder, label, onAdd, initial = "" }) {
  const [text, setText] = useState(initial);
  const { submit, busy, error } = useSubmit(async () => {
    await onAdd(text);
    setText("");
  });
  return (
    <form onSubmit={submit} className={styles.actions} style={{ justifyContent: "flex-start" }}>
      <input value={text} onChange={(e) => setText(e.target.value)} placeholder={placeholder} required />
      <button className={`btn btn-primary ${styles.small}`} disabled={busy}>
        {label !== "Save" && <Plus />} {label}
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
    <form onSubmit={submit} className={styles.actions} style={{ justifyContent: "flex-start", marginTop: 8 }}>
      <input type="file" accept=".md,.zip" multiple onChange={(e) => setFiles(e.target.files)} />
      <label>
        <input type="checkbox" checked={publish} onChange={(e) => setPublish(e.target.checked)} /> Publish now
      </label>
      <button className={`btn btn-primary ${styles.small}`} disabled={busy || !files.length}>
        {busy ? "Importing…" : "Import"}
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
    <section>
      <div className={styles.toolbar}>
        <p className="muted" style={{ margin: 0 }}>
          Build a quiz here, then show it in a lesson with a <em>Quiz</em> block. A final quiz must be passed to finish
          the course.
        </p>
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
