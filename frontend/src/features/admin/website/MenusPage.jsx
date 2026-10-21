import { ExternalLink, PanelBottom, PanelTop, Plus } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router";
import { useApi } from "../../../shared/hooks/useApi";
import { Field } from "../../../shared/ui/Field";
import { EditPanel, useResourceForm } from "../shared/EditPanel";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import { SortableList } from "../shared/SortableList";
import styles from "../shared/admin.module.css";
import pageStyles from "./MenusPage.module.css";
import { PAGES } from "./PagesPage";

export const MENUS = "/admin/website/menus";
const ITEMS = "/admin/website/menu-items";
const LOCATIONS = {
  header: {
    title: "Header",
    icon: PanelTop,
    hint: "The top bar of every page. A menu shows as a dropdown named after it, or as links side by side.",
  },
  footer: { title: "Footer", icon: PanelBottom, hint: "Each footer menu is one column, with its name on top." },
};
const SHOW_AS = {
  dropdown: "A dropdown: its name in the bar, its links under it",
  links: "Its links side by side in the bar",
};
const LINK_TYPES = { page: "A page", course: "A course", url: "A web address", none: "Nothing: a heading for a sub-menu" };

/** Admin -> Menus: the header links and the footer columns of the website. */
export function MenusPage() {
  const list = useApi(`${MENUS}/?page_size=500`);
  const [creating, setCreating] = useState(false);
  const menus = list.data?.results ?? [];

  return (
    <>
      <div className={styles.toolbar}>
        <h1>Menus</h1>
        <a className="btn btn-outline" href="/" target="_blank" rel="noreferrer">
          <ExternalLink /> View site
        </a>
        <button className="btn btn-primary" onClick={() => setCreating(true)}>
          <Plus /> New menu
        </button>
      </div>
      {creating && (
        <MenuForm initial={{ name: "", location: "header", show_as: "dropdown" }} onCancel={() => setCreating(false)}
          onSaved={() => { setCreating(false); list.reload(); }} />
      )}
      {Object.entries(LOCATIONS).map(([location, { title, icon: Icon, hint }]) => {
        const here = menus.filter((menu) => menu.location === location);
        return (
          <section key={location} style={{ marginBottom: 32 }}>
            <h2 style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <Icon size={22} /> {title}
            </h2>
            <p className="muted">
              {hint} Only active menus and links are shown. Use the arrows (or drag) to change the order. A link can hold a
              sub-menu: a dropdown in the header, an indented list in the footer.
            </p>
            {list.data && !here.length && <p className="muted">No {location} menu yet.</p>}
            <SortableList arrows items={here} base={MENUS} onChange={list.reload}
              renderItem={(menu) => <MenuCard menu={menu} onChange={list.reload} />} />
          </section>
        );
      })}
    </>
  );
}

function MenuForm({ initial, onSaved, onCancel }) {
  const form = useResourceForm(MENUS, initial, onSaved, (v) => ({
    name: v.name,
    location: v.location,
    show_as: v.show_as,
  }));
  const { values, onChange, error } = form;
  return (
    <EditPanel title={initial.id ? "Edit menu" : "New menu"} form={form} onCancel={onCancel}>
      <Field label="Name (the dropdown or footer column heading)" name="name" required value={values.name}
        onChange={onChange} error={error} placeholder="Games" />
      <Field label="Where it shows" name="location" as="select" value={values.location} onChange={onChange}
        error={error}>
        <option value="header">Header</option>
        <option value="footer">Footer column</option>
      </Field>
      {values.location === "header" && (
        <Field label="Show in the header as" name="show_as" as="select" value={values.show_as} onChange={onChange}
          error={error}>
          {Object.entries(SHOW_AS).map(([key, label]) => (
            <option key={key} value={key}>{label}</option>
          ))}
        </Field>
      )}
    </EditPanel>
  );
}

function MenuCard({ menu, onChange }) {
  const [editing, setEditing] = useState(false);
  const items = useApi(`${ITEMS}/?menu=${menu.id}&page_size=500`);
  const changed = () => {
    items.reload();
    onChange();
  };

  if (editing) {
    return <MenuForm initial={menu} onCancel={() => setEditing(false)} onSaved={() => { setEditing(false); onChange(); }} />;
  }
  return (
    <div>
      <div className={styles.toolbar} style={{ margin: "0 0 8px" }}>
        <span className={styles.grow}>
          <strong>{menu.name}</strong> <StatusBadge row={menu} />
          <span className="muted">
            {" · "}{menu.item_count} link{menu.item_count === 1 ? "" : "s"}
            {menu.location === "header" && (menu.show_as === "dropdown" ? " · dropdown" : " · links in the bar")}
          </span>
        </span>
        <RecordActions base={MENUS} row={menu} onChange={onChange} onEdit={() => setEditing(true)} />
      </div>
      <MenuItems menuId={menu.id} rows={items.data?.results ?? []} onChange={changed} />
    </div>
  );
}

function MenuItems({ menuId, rows, onChange }) {
  const [addingUnder, setAddingUnder] = useState(null);
  const top = rows.filter((item) => !item.parent);
  return (
    <LinkList menuId={menuId} rows={rows} items={top} onChange={onChange} addLabel="Add link"
      rowAction={(item) => (
        <button type="button" className={`btn btn-outline ${styles.small}`} title="Add a link to its sub-menu"
          onClick={() => setAddingUnder(item.id)}>
          <Plus /> Sub-link
        </button>
      )}
      renderBelow={(item) => {
        const children = rows.filter((child) => child.parent === item.id);
        if (!children.length && addingUnder !== item.id) return null;
        return (
          <div className={pageStyles.subMenu}>
            <LinkList menuId={menuId} rows={rows} parent={item} items={children} onChange={onChange}
              adding={addingUnder === item.id} onAddingDone={() => setAddingUnder(null)} />
          </div>
        );
      }} />
  );
}

/**
 * One level of links: the menu's top links, or the sub-menu of one link.
 * The top level has its own "Add link" button; a sub-menu is opened for a
 * new link by the "Sub-link" button of its parent row.
 */
function LinkList({ menuId, rows, items, parent, onChange, addLabel, adding: addingHere, onAddingDone,
  rowAction, renderBelow }) {
  const [editingId, setEditingId] = useState(null);
  const [addingOwn, setAddingOwn] = useState(false);
  const adding = addingOwn || addingHere;
  const stopAdding = () => {
    setAddingOwn(false);
    onAddingDone?.();
  };
  const done = () => {
    setEditingId(null);
    stopAdding();
    onChange();
  };
  const form = (item) => (
    <ItemForm menuId={menuId} item={item} parentId={item ? item.parent : parent?.id} onSaved={done}
      onCancel={() => (item ? setEditingId(null) : stopAdding())}
      parents={rows.filter((row) => !row.parent && row.id !== item?.id)}
      hasChildren={!!item && rows.some((row) => row.parent === item.id)} />
  );

  return (
    <>
      <SortableList arrows items={items} base={ITEMS} onChange={onChange}
        renderItem={(item) => (
          <>
            {editingId === item.id ? form(item) : (
              <div className={styles.toolbar} style={{ margin: 0 }}>
                <span className={styles.grow}>
                  {item.label ? <strong>{item.label}</strong> : <em className="muted">Title of the {item.link_type}</em>}{" "}
                  <StatusBadge row={item} />
                  {item.open_in_new_tab && <span className="muted" title="Opens in a new tab"> ↗</span>}
                  <div className="muted">{item.target}</div>
                </span>
                {rowAction?.(item)}
                <RecordActions base={ITEMS} row={item} onChange={onChange} onEdit={() => setEditingId(item.id)} />
              </div>
            )}
            {renderBelow?.(item)}
          </>
        )}
      />
      {adding && form(null)}
      {!adding && addLabel && (
        <button type="button" className={`btn btn-outline ${styles.small}`} onClick={() => setAddingOwn(true)}>
          <Plus /> {addLabel}
        </button>
      )}
    </>
  );
}

function ItemForm({ menuId, item, parentId, parents, hasChildren, onSaved, onCancel }) {
  const initial = {
    id: item?.id,
    parent: parentId ?? "",
    label: item?.label ?? "",
    link_type: item?.link_type ?? "page",
    page: item?.page ?? "",
    course_id: item?.course_id ?? "",
    url: item?.url ?? "",
    open_in_new_tab: item?.open_in_new_tab ?? false,
  };
  const form = useResourceForm(ITEMS, initial, onSaved, (v) => ({
    menu: menuId,
    parent: v.parent || null,
    label: v.label,
    link_type: v.link_type,
    page: v.link_type === "page" ? v.page || null : null,
    course_id: v.link_type === "course" ? v.course_id || null : null,
    url: v.link_type === "url" ? v.url : "",
    open_in_new_tab: v.link_type !== "none" && v.open_in_new_tab,
  }));
  const { values, onChange, setValues, error } = form;
  const kind = values.link_type;
  const types = Object.entries(LINK_TYPES).filter(([key]) => key !== "none" || !values.parent);

  return (
    <EditPanel title={item ? "Edit link" : values.parent ? "New sub-menu link" : "New link"} form={form}
      onCancel={onCancel}>
      {hasChildren ? (
        <p className="field muted">This link has a sub-menu, so it stays at the top level.</p>
      ) : (
        <Field label="Sits under" name="parent" as="select" value={values.parent} error={error}
          onChange={(e) => setValues({
            ...values,
            parent: e.target.value,
            link_type: e.target.value && kind === "none" ? "page" : kind,
          })}>
          <option value="">Top level of the menu</option>
          {parents.map((row) => (
            <option key={row.id} value={row.id}>Sub-menu of: {row.label || row.target}</option>
          ))}
        </Field>
      )}
      <Field label="Link to" name="link_type" as="select" value={kind} onChange={onChange} error={error}>
        {types.map(([key, label]) => (
          <option key={key} value={key}>{label}</option>
        ))}
      </Field>
      {kind === "page" && <PageSelect value={values.page} onChange={onChange} error={error} />}
      {kind === "course" && <CourseSelect value={values.course_id} onChange={onChange} error={error} />}
      {kind === "url" && (
        <Field label="Address" name="url" required value={values.url} onChange={onChange} error={error}
          placeholder="/courses or https://…" />
      )}
      <Field label={["url", "none"].includes(kind) ? "Label" : "Label (blank = the title)"} name="label"
        value={values.label} required={["url", "none"].includes(kind)} onChange={onChange} error={error}
        maxLength={100} placeholder={kind === "none" ? "Learn" : undefined} />
      {kind === "none" ? (
        <p className="muted" style={{ alignSelf: "center" }}>Opens its sub-menu. Add sub-links after saving.</p>
      ) : (
        <label style={{ alignSelf: "center" }}>
          <input type="checkbox" checked={values.open_in_new_tab}
            onChange={(e) => setValues({ ...values, open_in_new_tab: e.target.checked })} /> Open in a new tab
        </label>
      )}
    </EditPanel>
  );
}

function PageSelect({ value, onChange, error }) {
  const { data } = useApi(`${PAGES}/?page_size=500`);
  if (data && !data.results.length) {
    return (
      <p className="field">
        No pages yet. <Link to="/admin/pages/new">Write a page</Link> first.
      </p>
    );
  }
  return (
    <Field label="Page" name="page" as="select" required value={value} onChange={onChange} error={error}>
      <option value="">Choose…</option>
      {(data?.results ?? []).map((page) => (
        <option key={page.id} value={page.id}>
          {page.title} (/{page.slug}){page.is_active ? "" : " · hidden"}
        </option>
      ))}
    </Field>
  );
}

function CourseSelect({ value, onChange, error }) {
  const { data } = useApi("/admin/catalog/courses/?page_size=500");
  return (
    <Field label="Course" name="course_id" as="select" required value={value} onChange={onChange} error={error}>
      <option value="">Choose…</option>
      {(data?.results ?? []).map((course) => (
        <option key={course.id} value={course.id}>
          {course.title}{course.status === "published" && course.is_active ? "" : ` · ${course.status}`}
        </option>
      ))}
    </Field>
  );
}
