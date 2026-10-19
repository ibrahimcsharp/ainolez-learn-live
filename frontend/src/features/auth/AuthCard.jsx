import styles from "./AuthCard.module.css";

export function AuthCard({ title, children, footer }) {
  return (
    <div className={styles.wrap}>
      <section className={`card ${styles.card}`}>
        <h1 className={styles.title}>{title}</h1>
        {children}
      </section>
      {footer && <p className={styles.footer}>{footer}</p>}
    </div>
  );
}
