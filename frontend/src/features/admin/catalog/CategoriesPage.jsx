import { useState } from "react";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import { SortableList } from "../shared/SortableList";
import styles from "../shared/admin.module.css";

const BASE = "/admin/catalog/categories";
const NEW = { name: "", slug: "", icon: "", color: "#04AA6D", description: "" };

export function CategoriesPage() {
  const list = useApi(`${BASE}/?page_size=500`);
  const [editing, setEditing] = useState(null);

  function saved() {
    setEditing(null);
    list.reload();
  }

  return (
    <>
      <div className={styles.toolbar}>
        <h1>Categories</h1>
        <button className="btn btn-primary" onClick={() => setEditing(NEW)}>
          New category
        </button>
      </div>
      {editing && (
        <CategoryForm key={editing.id ?? "new"} initial={editing} onSaved={saved} onCancel={() => setEditing(null)} />
      )}
      <SortableList
        items={list.data?.results ?? []}
        base={BASE}
        onChange={list.reload}
        renderItem={(row) => (
          <div className={styles.toolbar} style={{ margin: 0 }}>
            <span>
              {row.icon} <strong>{row.name}</strong> <span className="muted">/{row.slug}</span>{" "}
              <StatusBadge row={row} />
            </span>
            <RecordActions base={BASE} row={row} onChange={list.reload} onEdit={setEditing} />
          </div>
        )}
      />
    </>
  );
}

function CategoryForm({ initial, onSaved, onCancel }) {
  const form = useResourceForm(BASE, initial, onSaved);
  const { values, onChange, error } = form;
  return (
    <EditPanel title={initial.id ? "Edit category" : "New category"} form={form} onCancel={onCancel}>
      <Field label="Name" name="name" required value={values.name} onChange={onChange} error={error} />
      <Field label="Slug (blank = from name)" name="slug" value={values.slug} onChange={onChange} error={error} />
      <Field label="Icon (emoji)" name="icon" value={values.icon} onChange={onChange} error={error} />
      <Field label="Colour" name="color" type="color" value={values.color} onChange={onChange} error={error} />
      <Field label="Description" name="description" value={values.description} onChange={onChange} error={error} />
    </EditPanel>
  );
}
