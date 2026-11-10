import { Plus, RotateCw } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { LoadingBar, Spinner } from "../../../shared/ui/Loader";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

export const COURSES = "/admin/catalog/courses";
export const LANGUAGES = [
  ["html", "HTML"], ["css", "CSS"], ["javascript", "JavaScript"], ["python", "Python"], ["sql", "SQL"],
  ["ai", "AI (no code)"], ["other", "Other"],
].map(([key, label]) => <option key={key} value={key}>{label}</option>);

/*
 * Every API call takes a few seconds, so the list loads once (without the long
 * descriptions) and search runs in the browser. The last list is kept for this tab, so
 * coming back from a course shows it at once while a fresh copy loads.
 */
const KEY = "ainolez.admin.courses";
let remembered = recall();

export function useCourseList() {
  const [state, setState] = useState({ rows: remembered, error: null, loading: true });
  const [version, setVersion] = useState(0);
  useEffect(() => {
    let live = true;
    setState((previous) => ({ ...previous, error: null, loading: true }));
    api(`${COURSES}/?page_size=500`)
      .then((data) => {
        remembered = data.results;
        try {
          sessionStorage.setItem(KEY, JSON.stringify(remembered));
        } catch {
          // storage full or blocked: the list still shows
        }
        if (live) setState({ rows: remembered, error: null, loading: false });
      })
      .catch((error) => live && setState((previous) => ({ ...previous, error, loading: false })));
    return () => {
      live = false;
    };
  }, [version]);
  return { ...state, reload: () => setVersion((v) => v + 1) };
}

function recall() {
  try {
    const rows = JSON.parse(sessionStorage.getItem(KEY));
    return Array.isArray(rows) ? rows : null;
  } catch {
    return null;
  }
}

export function matches(row, query) {
  const words = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const text = `${row.title} ${row.slug} ${row.category_name ?? ""} ${row.status}`.toLowerCase();
  return words.every((word) => text.includes(word));
}

export function CoursesPage() {
  const [query, setQuery] = useState("");
  const list = useCourseList();
  const [creating, setCreating] = useState(false);
  const navigate = useNavigate();
  const rows = list.rows?.filter((row) => matches(row, query));

  return (
    <>
      <LoadingBar done={!list.loading} />
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
      {list.error && (
        <p className="notice notice-error" role="alert">
          {list.rows ? "Couldn't refresh the list. It may be out of date. " : "Couldn't load the courses. "}
          <button className={`btn btn-outline ${styles.small}`} onClick={list.reload}>
            <RotateCw /> Try again
          </button>
        </p>
      )}
      <table className={styles.table} aria-busy={list.loading}>
        <thead>
          <tr>
            <th>Course</th>
            <th>Category</th>
            <th>Status</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {!rows && !list.error && <SkeletonRows />}
          {rows?.map((row) => (
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
          {rows && !rows.length && (
            <tr>
              <td colSpan={4} className={styles.emptyRow}>
                {list.rows.length ? `No course matches “${query}”.` : "No courses yet. Press New course to add one."}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  );
}

/** Grey placeholder rows with a spinner while the first list loads. */
function SkeletonRows() {
  return (
    <>
      <tr>
        <td colSpan={4} className={styles.loadingRow}>
          <Spinner size={22} label="Loading courses" /> Loading courses…
        </td>
      </tr>
      {[70, 55, 80, 60, 45].map((width) => (
        <tr key={width} className={styles.skeletonRow} aria-hidden>
          <td>
            <span style={{ width: `${width}%` }} />
            <span style={{ width: "30%" }} />
          </td>
          <td>
            <span />
          </td>
          <td>
            <span style={{ width: 64 }} />
          </td>
          <td />
        </tr>
      ))}
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
