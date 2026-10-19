import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

export const COURSES = "/admin/catalog/courses";

export function CoursesPage() {
  const [query, setQuery] = useState("");
  const list = useApi(`${COURSES}/?page_size=500&q=${encodeURIComponent(query)}`);
  const [creating, setCreating] = useState(false);
  const navigate = useNavigate();

  return (
    <>
      <div className={styles.toolbar}>
        <h1>Courses</h1>
        <input type="search" placeholder="Search courses" value={query} onChange={(e) => setQuery(e.target.value)} />
        <button className="btn btn-primary" onClick={() => setCreating(true)}>
          New course
        </button>
      </div>
      {creating && (
        <NewCourseForm onSaved={(course) => navigate(`/admin/courses/${course.id}`)} onCancel={() => setCreating(false)} />
      )}
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Course</th>
            <th>Category</th>
            <th>Status</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {(list.data?.results ?? []).map((row) => (
            <tr key={row.id}>
              <td>
                <Link to={`/admin/courses/${row.id}`}>{row.title}</Link>
                <div className="muted">/{row.slug}</div>
              </td>
              <td>{row.category_name}</td>
              <td>
                <StatusBadge row={row} />
              </td>
              <td>
                <RecordActions base={COURSES} row={row} onChange={list.reload} onEdit={() => navigate(`/admin/courses/${row.id}`)} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

function NewCourseForm({ onSaved, onCancel }) {
  const form = useResourceForm(COURSES, { title: "", category: "" }, onSaved);
  return (
    <EditPanel title="New course" form={form} onCancel={onCancel}>
      <CategorySelect value={form.values.category} onChange={form.onChange} error={form.error} />
      <Field label="Title" name="title" required value={form.values.title} onChange={form.onChange} error={form.error} />
    </EditPanel>
  );
}

export function CategorySelect({ value, onChange, error }) {
  const { data } = useApi("/admin/catalog/categories/?page_size=500");
  return (
    <Field label="Category" name="category" as="select" required value={value} onChange={onChange} error={error}>
      <option value="">Choose…</option>
      {(data?.results ?? []).map((category) => (
        <option key={category.id} value={category.id}>
          {category.name}
        </option>
      ))}
    </Field>
  );
}
