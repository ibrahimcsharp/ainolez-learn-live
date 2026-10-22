import { ArrowLeft, Download, ExternalLink, Eye, Pencil, Rocket, Undo2 } from "lucide-react";
import { useState } from "react";
import { Link, useParams } from "react-router";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { useSubmit } from "../../../shared/hooks/useForm";
import { Field } from "../../../shared/ui/Field";
import { LessonContent } from "../../lesson/LessonContent";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";
import { SeoEditor } from "../seo/SeoEditor";
import { BlocksEditor } from "./BlocksEditor";

const LESSONS = "/admin/catalog/lessons";

export function LessonEditPage() {
  const { id } = useParams();
  const lesson = useApi(`${LESSONS}/${id}/`);
  const blocks = useApi(`/admin/catalog/blocks/?lesson=${id}&page_size=500`);
  const [preview, setPreview] = useState(false);
  if (!lesson.data) return <p className={lesson.error ? "page-loading" : "page-loading is-loading"}>{lesson.error?.message ?? "Loading…"}</p>;
  const { data } = lesson;

  async function exportMarkdown() {
    const response = await api(`${LESSONS}/${id}/export/`, { raw: true });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(await response.blob());
    link.download = `${data.slug}.md`;
    link.click();
    URL.revokeObjectURL(link.href);
  }

  return (
    <>
      <Link to={`/admin/courses/${data.course}`} className={styles.back}>
        <ArrowLeft size={16} /> Back to the course
      </Link>
      <div className={styles.toolbar}>
        <h1>
          {data.title} <StatusBadge row={data} />
        </h1>
        <div className={styles.actions}>
          {data.status === "published" && (
            <a className="btn btn-outline" href={`/${data.course_slug}/${data.slug}`}>
              <ExternalLink /> View on site
            </a>
          )}
          <button className="btn btn-outline" onClick={exportMarkdown}>
            <Download /> Export .md
          </button>
          <button className="btn btn-outline" aria-pressed={preview} onClick={() => setPreview(!preview)}>
            {preview ? <><Pencil /> Edit blocks</> : <><Eye /> Preview</>}
          </button>
          <PublishButton lesson={data} onDone={lesson.reload} />
        </div>
      </div>
      <details className={styles.panel}>
        <summary><strong>Lesson settings</strong> <span className="muted">title, web address, minutes, summary</span></summary>
        <LessonForm key={data.updated_at} initial={data} onSaved={lesson.reload} />
      </details>
      <details className={styles.panel}>
        <summary><strong>SEO and social sharing</strong></summary>
        <SeoEditor key={data.slug} path={`/${data.course_slug}/${data.slug}`} />
      </details>
      {preview ? (
        <div className={`card ${styles.preview}`}>
          <h1>{data.title}</h1>
          <LessonContent blocks={(blocks.data?.results ?? []).filter((block) => block.is_active)} />
        </div>
      ) : (
        <BlocksEditor lessonId={Number(id)} courseId={data.course} blocks={blocks.data?.results ?? []}
          onChange={blocks.reload} />
      )}
    </>
  );
}

function PublishButton({ lesson, onDone }) {
  const live = lesson.status === "published";
  const { submit, busy, error } = useSubmit(async () => {
    await api(`${LESSONS}/${lesson.id}/`, { method: "PATCH", body: { status: live ? "draft" : "published" } });
    onDone();
  });
  return (
    <>
      {error && <span className={styles.danger}>{error.message}</span>}
      <button className={live ? "btn btn-outline" : "btn btn-primary"} disabled={busy} onClick={submit}>
        {live ? <><Undo2 /> Unpublish</> : <><Rocket /> Publish lesson</>}
      </button>
    </>
  );
}

function LessonForm({ initial, onSaved }) {
  const form = useResourceForm(LESSONS, initial, onSaved);
  const { values, onChange, error } = form;
  return (
    <EditPanel form={form}>
      <Field label="Title" name="title" required value={values.title} onChange={onChange} error={error} />
      <Field label="Web address (slug)" name="slug" value={values.slug} onChange={onChange} error={error} />
      <Field label="Minutes" name="estimated_minutes" type="number" min="1" value={values.estimated_minutes}
        onChange={onChange} error={error} />
      <Field label="Summary" name="summary" value={values.summary} onChange={onChange} error={error} />
    </EditPanel>
  );
}
