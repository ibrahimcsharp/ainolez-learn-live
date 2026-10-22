import { ArrowLeft, Eye, FolderOpen, Plus, RotateCcw, Save, Sparkles, Trash2, Wand2, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useFormFields, useSubmit } from "../../../shared/hooks/useForm";
import { Field, FormError } from "../../../shared/ui/Field";
import { AISwitch } from "../shared/AISwitch";
import styles from "../shared/admin.module.css";

const JOBS = "/admin/ai-authoring/jobs";
const BUSY = ["outline_queued", "generating"];
const STATUS = {
  outline_queued: "Writing the outline…",
  outline_ready: "Outline ready for review",
  generating: "Writing lessons…",
  drafted: "Draft course ready",
  failed: "Needs attention",
};

/** PLANNING.md 6.7: Claude drafts a course, the admin reviews every step. */
export function CourseGeneratorPage() {
  const list = useApi(`${JOBS}/?page_size=50`);
  const [openId, setOpenId] = useState(null);
  return (
    <>
      <h1>AI course generator</h1>
      <AISwitch name="course_generator_enabled" icon={Sparkles} title="The AI course generator"
        on="Admins can start new AI-drafted courses."
        off="No new outlines or lessons can be started. Courses already drafted stay as they are." />
      <p className="muted">
        Claude proposes an outline, you edit it, then Claude drafts each lesson with examples, an exercise and a quiz.
        Everything stays a draft until you publish it. Background jobs run every minute (cron).
      </p>
      {openId ? (
        <JobDetail id={openId} onBack={() => { setOpenId(null); list.reload(); }} />
      ) : (
        <>
          <NewJobForm onStarted={(job) => setOpenId(job.id)} />
          <table className={styles.table}>
            <thead>
              <tr><th>Topic</th><th>Status</th><th>Lessons</th><th>Cost</th><th /></tr>
            </thead>
            <tbody>
              {(list.data?.results ?? []).map((job) => (
                <tr key={job.id}>
                  <td>{job.outline?.title ?? job.topic}</td>
                  <td>{STATUS[job.status]}</td>
                  <td>{job.lessons_total ? `${job.lessons_done} / ${job.lessons_total}` : "–"}</td>
                  <td>${Number(job.cost_usd).toFixed(2)}</td>
                  <td>
                    <button className={`btn btn-outline ${styles.small}`} onClick={() => setOpenId(job.id)}><FolderOpen /> Open</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </>
  );
}

function NewJobForm({ onStarted }) {
  const [values, onChange] = useFormFields({
    topic: "", level: "beginner", audience: "", language_key: "python", category_id: "",
    chapters_count: 6, lessons_per_chapter: 4, notes: "",
  });
  const { submit, busy, error } = useSubmit(async () => {
    onStarted(await api(`${JOBS}/`, { method: "POST", body: { ...values, category_id: values.category_id || null } }));
  });
  return (
    <form className={`card ${styles.panel}`} onSubmit={submit}>
      <h3>New course</h3>
      <FormError error={error} />
      <Field label="Topic" name="topic" required value={values.topic} onChange={onChange} error={error}
        placeholder="Python for Absolute Beginners" />
      <div className={styles.formGrid}>
        <Field label="Level" name="level" as="select" value={values.level} onChange={onChange}>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </Field>
        <Field label="Code language" name="language_key" as="select" value={values.language_key} onChange={onChange}>
          {["python", "sql", "html", "css", "javascript", "ai", "other"].map((key) => <option key={key}>{key}</option>)}
        </Field>
        <CategoryField value={values.category_id} onChange={onChange} />
        <Field label="Chapters" name="chapters_count" type="number" min="1" max="15" value={values.chapters_count}
          onChange={onChange} error={error} />
        <Field label="Lessons per chapter" name="lessons_per_chapter" type="number" min="1" max="10"
          value={values.lessons_per_chapter} onChange={onChange} error={error} />
      </div>
      <Field label="Audience" name="audience" value={values.audience} onChange={onChange}
        placeholder="Complete beginners who have never written code" />
      <Field label="Notes for Claude (optional)" name="notes" as="textarea" rows={2} value={values.notes}
        onChange={onChange} placeholder="End with a small project. Use pandas from chapter 3." />
      <button className="btn btn-primary" disabled={busy}><Sparkles /> {busy ? "Starting…" : "Propose an outline"}</button>
    </form>
  );
}

function CategoryField({ value, onChange }) {
  const { data } = useApi("/admin/catalog/categories/?page_size=200");
  return (
    <Field label="Category" name="category_id" as="select" value={value ?? ""} onChange={onChange}>
      <option value="">— pick later —</option>
      {(data?.results ?? []).map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
    </Field>
  );
}

function JobDetail({ id, onBack }) {
  const job = useApi(`${JOBS}/${id}/`);
  const status = job.data?.status;
  useEffect(() => {
    if (!BUSY.includes(status)) return undefined;
    const timer = setInterval(job.reload, 5000); // the jobs run in the background
    return () => clearInterval(timer);
  }, [status]); // job.reload changes every render; the status decides

  if (!job.data) return <p className={job.error ? "page-loading" : "page-loading is-loading"}>{job.error?.message ?? "Loading…"}</p>;
  const data = job.data;

  async function run(action) {
    try {
      await api(`${JOBS}/${id}/${action}/`, { method: "POST" });
      job.reload();
    } catch (error) {
      alert(error.message);
    }
  }

  return (
    <>
      <button className={`btn btn-outline ${styles.small}`} onClick={onBack}><ArrowLeft /> All courses</button>
      <section className={`card ${styles.panel}`}>
        <div className={styles.toolbar}>
          <h2 style={{ margin: 0 }}>{data.outline?.title ?? data.topic}</h2>
          <strong>{STATUS[status]}</strong>
        </div>
        <p className="muted">
          {data.level} · {data.language_key} · {data.tokens_in + data.tokens_out} tokens · $
          {Number(data.cost_usd).toFixed(2)}
        </p>
        {data.error && <p className="notice notice-error">{data.error}</p>}
        {status === "outline_queued" && <p>Claude is planning the course. This page refreshes on its own.</p>}
        {data.lessons_total > 0 && (
          <p>
            <progress max={data.lessons_total} value={data.lessons_done} /> {data.lessons_done} of {data.lessons_total}{" "}
            lessons written{data.lessons_failed ? `, ${data.lessons_failed} failed` : ""}
          </p>
        )}
        <div className={styles.actions} style={{ justifyContent: "flex-start" }}>
          {data.course_id && (
            <Link className="btn btn-primary" to={`/admin/courses/${data.course_id}`}><Eye /> Review the draft course</Link>
          )}
          {status === "failed" && <button className="btn btn-outline" onClick={() => run("retry")}><RotateCcw /> Retry</button>}
        </div>
      </section>
      {status === "outline_ready" && <OutlineEditor job={data} onChange={job.reload} onGenerate={() => run("generate")} />}
    </>
  );
}

function OutlineEditor({ job, onChange, onGenerate }) {
  const [outline, setOutline] = useState(job.outline);
  const [category, setCategory] = useState(job.category_id ?? "");
  const { submit, busy, error } = useSubmit(async () => {
    await api(`${JOBS}/${job.id}/`, { method: "PATCH", body: { category_id: category || null } });
    await api(`${JOBS}/${job.id}/outline/`, { method: "PATCH", body: { outline } });
    onChange();
  });
  const update = (change) => setOutline({ ...outline, ...change });
  const updateChapter = (index, change) =>
    update({ chapters: outline.chapters.map((c, i) => (i === index ? { ...c, ...change } : c)) });
  const updateLesson = (ci, li, change) =>
    updateChapter(ci, { lessons: outline.chapters[ci].lessons.map((l, i) => (i === li ? { ...l, ...change } : l)) });
  const remove = (list, index) => list.filter((_, i) => i !== index);

  async function saveAndGenerate() {
    await submit();
    if (confirm("Write all lessons now? Each lesson is one Claude call.")) onGenerate();
  }

  return (
    <form className="card" onSubmit={submit}>
      <h3>Review the outline</h3>
      <FormError error={error} />
      <div className={styles.formGrid}>
        <Field label="Course title" name="title" value={outline.title} onChange={(e) => update({ title: e.target.value })} />
        <CategoryField value={category} onChange={(e) => setCategory(e.target.value)} />
      </div>
      <Field label="Short description" name="short_description" value={outline.short_description}
        onChange={(e) => update({ short_description: e.target.value })} />
      <Field label="Description" name="description" as="textarea" rows={3} value={outline.description}
        onChange={(e) => update({ description: e.target.value })} />

      {outline.chapters.map((chapter, ci) => (
        <fieldset key={ci} className={styles.panel} style={{ border: "1px solid var(--gray-200)", borderRadius: 8 }}>
          <legend>Chapter {ci + 1}</legend>
          <div className={styles.toolbar}>
            <input value={chapter.title} aria-label="Chapter title" style={{ flex: 1, fontWeight: 600 }}
              onChange={(e) => updateChapter(ci, { title: e.target.value })} />
            <button type="button" className={`btn btn-outline ${styles.small} ${styles.danger}`}
              onClick={() => update({ chapters: remove(outline.chapters, ci) })}><Trash2 /> Remove chapter</button>
          </div>
          {chapter.lessons.map((lesson, li) => (
            <div key={li} className={styles.toolbar}>
              <input value={lesson.title} aria-label="Lesson title" style={{ width: 240 }}
                onChange={(e) => updateLesson(ci, li, { title: e.target.value })} />
              <input value={lesson.summary} aria-label="Lesson summary" style={{ flex: 1 }}
                onChange={(e) => updateLesson(ci, li, { summary: e.target.value })} />
              <button type="button" className={`btn btn-outline ${styles.small}`}
                onClick={() => updateChapter(ci, { lessons: remove(chapter.lessons, li) })} aria-label="Remove lesson"><X /></button>
            </div>
          ))}
          <button type="button" className={`btn btn-outline ${styles.small}`}
            onClick={() => updateChapter(ci, { lessons: [...chapter.lessons, { title: "", summary: "" }] })}>
            <Plus /> Lesson
          </button>
        </fieldset>
      ))}
      <div className={styles.actions} style={{ justifyContent: "flex-start" }}>
        <button type="button" className="btn btn-outline"
          onClick={() => update({ chapters: [...outline.chapters, { title: "New chapter", description: "", lessons: [] }] })}>
          <Plus /> Chapter
        </button>
        <button className="btn btn-outline" disabled={busy}><Save /> Save outline</button>
        <button type="button" className="btn btn-primary" disabled={busy || !category} onClick={saveAndGenerate}>
          <Wand2 /> Write the lessons
        </button>
        {!category && <span className="muted">Pick a category first.</span>}
      </div>
    </form>
  );
}
