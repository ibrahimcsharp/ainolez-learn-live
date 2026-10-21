import { ArrowUpRight, ChevronDown, ChevronRight } from "lucide-react";
import { useEffect, useId, useRef, useState } from "react";
import { useLocation } from "react-router";
import { MenuLink } from "./MenuLink";
import styles from "./MenuDropdown.module.css";

/**
 * A header link with a sub-menu. Hover opens it with a mouse; the arrow
 * button (or the label, for a heading with no link) opens it by click, tap
 * or keyboard. Escape, a click outside or opening a page closes it.
 */
export function MenuDropdown({ link }) {
  const [open, setOpen] = useState(false);
  const [top, setTop] = useState(0);
  const box = useRef(null);
  const button = useRef(null);
  const id = useId();
  const { pathname } = useLocation();

  useEffect(() => setOpen(false), [pathname]);
  useEffect(() => {
    if (!open) return undefined;
    const outside = (event) => box.current?.contains(event.target) || setOpen(false);
    const key = (event) => {
      if (event.key === "Escape") {
        setOpen(false);
        button.current?.focus();
      }
    };
    const close = () => setOpen(false);
    document.addEventListener("pointerdown", outside);
    document.addEventListener("keydown", key);
    window.addEventListener("scroll", close, { passive: true });
    window.addEventListener("resize", close);
    return () => {
      document.removeEventListener("pointerdown", outside);
      document.removeEventListener("keydown", key);
      window.removeEventListener("scroll", close);
      window.removeEventListener("resize", close);
    };
  }, [open]);

  function toggle() {
    // On phones the header scrolls sideways, so the panel is placed below it (see css).
    setTop(box.current?.getBoundingClientRect().bottom ?? 0);
    setOpen(!open);
  }

  const trigger = (
    <button ref={button} type="button" className={styles.toggle} aria-expanded={open} aria-controls={id}
      onClick={toggle} aria-label={link.url ? `${link.label} menu` : undefined}>
      {!link.url && link.label}
      <ChevronDown size={16} aria-hidden className={styles.chevron} />
    </button>
  );
  return (
    <div ref={box} className={styles.dropdown} data-open={open}>
      {link.url ? (
        <span className={styles.split}>
          <MenuLink link={link} />
          {trigger}
        </span>
      ) : (
        trigger
      )}
      <div id={id} className={styles.panel} style={{ "--panel-top": `${top}px` }}>
        <ul className={styles.list}>
          {link.children.map((child, i) => (
            <li key={`${child.label}-${i}`} className={child.children ? styles.group : undefined}>
              {child.url ? (
                <PanelLink link={child} current={pathname} />
              ) : (
                <span className={styles.heading}>{child.label}</span>
              )}
              {child.children && (
                <ul className={styles.nested}>
                  {child.children.map((sub, j) => (
                    <li key={`${sub.url}-${j}`}>
                      <PanelLink link={sub} current={pathname} />
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

/** One row of the panel: the label, and an arrow (or a new-tab mark) on the right. */
function PanelLink({ link, current }) {
  const here = link.url === current;
  return (
    <MenuLink link={link} className={styles.item} aria-current={here ? "page" : undefined}>
      <span>{link.label}</span>
      {link.new_tab ? (
        <>
          <span className={styles.hidden}> (opens in a new tab)</span>
          <ArrowUpRight size={15} aria-hidden className={styles.icon} />
        </>
      ) : (
        <ChevronRight size={15} aria-hidden className={styles.icon} />
      )}
    </MenuLink>
  );
}
