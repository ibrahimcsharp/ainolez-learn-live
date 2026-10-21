import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";
import { api } from "../../../shared/api/client";
import styles from "./admin.module.css";

/**
 * Drag-and-drop list. After a drop it saves the new order with POST `${base}/reorder/`.
 * `renderItem(item)` draws one row. `arrows` adds Move up / Move down buttons,
 * for ordering without dragging (and from the keyboard).
 */
export function SortableList({ items, base, onChange, renderItem, arrows = false }) {
  const [dragged, setDragged] = useState(null);
  const [saving, setSaving] = useState(false);

  async function save(ids) {
    setSaving(true);
    try {
      await api(`${base}/reorder/`, { method: "POST", body: { ids } });
    } finally {
      setSaving(false);
    }
    onChange();
  }

  async function drop(target) {
    if (dragged === null || dragged === target.id) return;
    const ids = items.map((item) => item.id).filter((id) => id !== dragged);
    ids.splice(ids.indexOf(target.id), 0, dragged);
    setDragged(null);
    await save(ids);
  }

  function move(index, step) {
    const ids = items.map((item) => item.id);
    [ids[index], ids[index + step]] = [ids[index + step], ids[index]];
    save(ids);
  }

  return (
    <ul className={styles.sortable}>
      {items.map((item, index) => (
        <li
          key={item.id}
          className={styles.sortableItem}
          data-dragging={dragged === item.id}
          draggable
          // stopPropagation keeps a list nested inside another (lessons in chapters) separate
          onDragStart={(event) => {
            event.stopPropagation();
            setDragged(item.id);
          }}
          onDragEnd={() => setDragged(null)}
          onDragOver={(event) => event.preventDefault()}
          onDrop={(event) => {
            event.stopPropagation();
            drop(item);
          }}
        >
          {arrows ? (
            <span className={styles.order}>
              <button type="button" title="Move up" aria-label="Move up" disabled={saving || index === 0}
                onClick={() => move(index, -1)}>
                <ChevronUp size={16} />
              </button>
              <button type="button" title="Move down" aria-label="Move down"
                disabled={saving || index === items.length - 1} onClick={() => move(index, 1)}>
                <ChevronDown size={16} />
              </button>
            </span>
          ) : (
            <span className={styles.handle} title="Drag to reorder" aria-hidden>
              ⠿
            </span>
          )}
          <div className={styles.grow}>{renderItem(item)}</div>
        </li>
      ))}
    </ul>
  );
}
