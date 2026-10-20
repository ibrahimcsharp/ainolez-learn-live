import { useState } from "react";
import { api } from "../../../shared/api/client";
import styles from "./admin.module.css";

/**
 * Drag-and-drop list. After a drop it saves the new order with POST `${base}/reorder/`.
 * `renderItem(item)` draws one row.
 */
export function SortableList({ items, base, onChange, renderItem }) {
  const [dragged, setDragged] = useState(null);

  async function drop(target) {
    if (dragged === null || dragged === target.id) return;
    const ids = items.map((item) => item.id).filter((id) => id !== dragged);
    ids.splice(ids.indexOf(target.id), 0, dragged);
    setDragged(null);
    await api(`${base}/reorder/`, { method: "POST", body: { ids } });
    onChange();
  }

  return (
    <ul className={styles.sortable}>
      {items.map((item) => (
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
          <span className={styles.handle} title="Drag to reorder" aria-hidden>
            ⠿
          </span>
          <div className={styles.grow}>{renderItem(item)}</div>
        </li>
      ))}
    </ul>
  );
}
