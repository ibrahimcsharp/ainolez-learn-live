import { ChevronRight, Link2, PanelBottom, PanelTop, Plus, Trash2 } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router";
import { api } from "../../../shared/api/client";
import { useApi } from "../../../shared/hooks/useApi";
import { FormError } from "../../../shared/ui/Field";
import { StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";
import pageStyles from "./PageEditPage.module.css";
import { MENUS } from "./MenusPage";

const ITEMS = "/admin/website/menu-items";

/**
 * The page editor's Menus tab: where the page is linked, and a quick way to add
 * it to any menu, at the top level or under one of its links (a sub-menu).
 */
export function PageMenus({ page }) {
  const menus = useApi(`${MENUS}/?page_size=500`);
  const items = useApi(`${ITEMS}/?page_size=500`);
  const [menuId, setMenuId] = useState("");
  const [parentId, setParentId] = useState("");
  const [label, setLabel] = useState(page.title);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  if (!menus.data || !items.data) {
    const failed = menus.error ?? items.error;
    return <p className={failed ? "page-loading" : "page-loading is-loading"}>{failed?.message ?? "Loading…"}</p>;
  }
  const allMenus = menus.data.results;
  const allItems = items.data.results;
  const menuOf = (id) => allMenus.find((m) => m.id === id);
  const itemOf = (id) => allItems.find((i) => i.id === id);
  const linked = allItems.filter((item) => item.page === page.id);
  const parents = allItems.filter((item) => item.menu === Number(menuId) && item.parent === null);

  async function add(event) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await api(`${ITEMS}/`, {
        method: "POST",
        body: {
          menu: Number(menuId), parent: parentId ? Number(parentId) : null,
          link_type: "page", page: page.id, label: label.trim(),
        },
      });
      setParentId("");
      items.reload();
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }

  async function remove(item) {
    if (!window.confirm(`Remove the "${item.label || page.title}" link from ${menuOf(item.menu)?.name}?`)) return;
    try {
      await api(`${ITEMS}/${item.id}/soft-delete/`, { method: "POST" });
      items.reload();
    } catch (err) {
      setError(err);
    }
  }

  return (
    <section className="card">
      <h3>Where this page is linked</h3>
      {!page.is_active && (
        <p className="notice notice-info">This page is hidden, so its links do not show on the site yet.</p>
      )}
      {linked.length === 0 && <p className="muted">Not in any menu yet. Add it below.</p>}
      <ul className={pageStyles.links}>
        {linked.map((item) => {
          const menu = menuOf(item.menu);
          const parent = item.parent ? itemOf(item.parent) : null;
          const Icon = menu?.location === "footer" ? PanelBottom : PanelTop;
          return (
            <li key={item.id} className={pageStyles.link}>
              <Icon size={18} className="muted" />
              <span className={pageStyles.path}>
                <span className={pageStyles.where}>{menu?.location}</span>
                <strong>{menu?.name}</strong>
                {parent && <><ChevronRight size={14} /> {parent.label || parent.target}</>}
                <ChevronRight size={14} /> {item.label || page.title}
                <StatusBadge row={item} />
              </span>
              <button type="button" className={`btn btn-outline ${styles.small} ${styles.danger}`}
                onClick={() => remove(item)}>
                <Trash2 /> Remove
              </button>
            </li>
          );
        })}
      </ul>

      <h3>Add to a menu</h3>
      {allMenus.length === 0 ? (
        <p className="muted">
          There are no menus yet. Make one in <Link to="/admin/menus">Menus</Link>.
        </p>
      ) : (
        <form onSubmit={add}>
          <FormError error={error} />
          <div className={pageStyles.addForm}>
            <div className="field">
              <label htmlFor="menu-pick">Menu</label>
              <select id="menu-pick" required value={menuId}
                onChange={(e) => { setMenuId(e.target.value); setParentId(""); }}>
                <option value="">Choose a menu…</option>
                {["header", "footer"].map((location) => (
                  <optgroup key={location} label={location === "header" ? "Header" : "Footer"}>
                    {allMenus.filter((m) => m.location === location).map((m) => (
                      <option key={m.id} value={m.id}>{m.name}</option>
                    ))}
                  </optgroup>
                ))}
              </select>
            </div>
            <div className="field">
              <label htmlFor="parent-pick">Place</label>
              <select id="parent-pick" value={parentId} disabled={!menuId} onChange={(e) => setParentId(e.target.value)}>
                <option value="">Top level of the menu</option>
                {parents.map((p) => (
                  <option key={p.id} value={p.id}>Sub-menu of “{p.label || p.target}”</option>
                ))}
              </select>
            </div>
            <div className="field">
              <label htmlFor="label-pick">Link text</label>
              <input id="label-pick" value={label} maxLength={100} placeholder={page.title}
                onChange={(e) => setLabel(e.target.value)} />
            </div>
            <div className="field">
              <button className="btn btn-primary" disabled={busy || !menuId}>
                {busy ? <Link2 /> : <Plus />} {busy ? "Adding…" : "Add link"}
              </button>
            </div>
          </div>
          <p className="muted">
            To change the order, use <Link to="/admin/menus">Menus</Link>.
          </p>
        </form>
      )}
    </section>
  );
}
