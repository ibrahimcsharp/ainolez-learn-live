import styles from "./Loader.module.css";

/** A turning ring in the brand greens. */
export function Spinner({ size = 40, label = "Loading" }) {
  return (
    <span className={styles.spinner} style={{ "--size": `${size}px` }} role="status" aria-label={label} />
  );
}

/**
 * A thin bar along the top of the screen (or of its parent, with `inline`).
 * It creeps forward while loading and runs to the end and fades out when `done`.
 */
export function LoadingBar({ done = false, inline = false }) {
  return (
    <div className={`${styles.bar} ${inline ? styles.inline : ""}`} data-done={done} aria-hidden>
      <span className={styles.fill} />
    </div>
  );
}

/** What a page shows while its content loads: the bar plus a spinner and a label. */
export function PageLoader({ label = "Loading…", hint }) {
  return (
    <div className={styles.page}>
      <LoadingBar />
      <Spinner size={44} label={label} />
      <p className={styles.label}>{label}</p>
      {hint && <p className={styles.hint}>{hint}</p>}
    </div>
  );
}
