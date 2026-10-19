import { useState } from "react";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

const BASE = "/admin/catalog/paths";
const NEW = { title: "", slug: "", level: "beginner", description: "", course_ids: [] };

export function PathsPage() {
  const list = useApi(`${BASE}/?page_size=500`);
  const courses = useApi("/admin/catalog/courses/?page_size=500");
  const [editing, setEditing] = useState(null);
  const courseTitle = Object.fromEntries((courses.data?.results ?? []).map((c) => [c.id, c.title]));

  return (
    <>
      <div className={styles.toolbar}>
        <h1>Learning paths</h1>
        <button className="btn btn-primary" onClick={() => setEditing(NEW)}>
          New path
        </button>
      </div>
      {editing && (
        <PathForm
          key={editing.id ?? "new"}
          initial={editing}
          courses={courses.data?.results ?? []}
          onSaved={() => {
            setEditing(null);
            list.reload();
          }}
          onCancel={() => setEditing(null)}
        />
      )}
      <table className={styles.table}>
        <tbody>
          {(list.data?.results ?? []).map((row) => (
            <tr key={row.id}>
              <td>
                <strong>{row.title}</strong> <StatusBadge row={row} />
                <div className="muted">{row.course_ids.map((id) => courseTitle[id]).join(" → ")}</div>
              </td>
              <td>
                <RecordActions base={BASE} row={row} onChange={list.reload} onEdit={setEditing} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

function PathForm({ initial, courses, onSaved, onCancel }) {
  const form = useResourceForm(BASE, initial, onSaved);
  const { values, onChange, setValues, error } = form;
  const chosen = values.course_ids;

  function toggle(id) {
    const course_ids = chosen.includes(id) ? chosen.filter((c) => c !== id) : [...chosen, id];
    setValues({ ...values, course_ids });
  }

  return (
    <EditPanel title={initial.id ? "Edit path" : "New path"} form={form} onCancel={onCancel}>
      <Field label="Title" name="title" required value={values.title} onChange={onChange} error={error} />
      <Field label="Slug" name="slug" value={values.slug} onChange={onChange} error={error} />
      <Field label="Level" name="level" as="select" value={values.level} onChange={onChange} error={error}>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </Field>
      <Field label="Description" name="description" value={values.description} onChange={onChange} error={error} />
      <fieldset style={{ gridColumn: "1 / -1" }}>
        <legend>Courses (in the order you tick them)</legend>
        {courses.map((course) => (
          <label key={course.id} style={{ display: "block" }}>
            <input type="checkbox" checked={chosen.includes(course.id)} onChange={() => toggle(course.id)} />{" "}
            {chosen.includes(course.id) && <strong>{chosen.indexOf(course.id) + 1}. </strong>}
            {course.title}
          </label>
        ))}
      </fieldset>
    </EditPanel>
  );
}
