import { Plus } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

export const COURSES = "/admin/catalog/courses";
export const LANGUAGES = [
  ["html", "HTML"], ["css", "CSS"], ["javascript", "JavaScript"], ["python", "Python"], ["sql", "SQL"],
  ["ai", "AI (no code)"], ["other", "Other"],
].map(([key, label]) => <option key={key} value={key}>{label}</option>);

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
          <Plus /> New course
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

/** Step 1 of a course: the basics. The course page then guides through chapters and lessons. */
function NewCourseForm({ onSaved, onCancel }) {
  const blank = { title: "", category: "", level: "beginner", language_key: "python", short_description: "" };
  const form = useResourceForm(COURSES, blank, onSaved);
  const { values, onChange, error } = form;
  return (
    <EditPanel title="New course" form={form} onCancel={onCancel}>
      <Field label="Course title" name="title" required value={values.title} onChange={onChange} error={error}
        placeholder="Python for Beginners" />
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
      <div style={{ gridColumn: "1 / -1" }}>
        <Field label="One-line description (optional)" name="short_description" value={values.short_description}
          onChange={onChange} error={error} />
        <p className="muted">The course starts as a draft. Next you add chapters and lessons, then press Publish.</p>
      </div>
    </EditPanel>
  );
}

export function CategorySelect({ value, onChange, error }) {
  const { data } = useApi("/admin/catalog/categories/?page_size=500");
  if (data && !data.results.length) {
    return (
      <p className="field">
        No categories yet. <Link to="/admin/categories">Add a category</Link> first (for example “Web Development”).
      </p>
    );
  }
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
