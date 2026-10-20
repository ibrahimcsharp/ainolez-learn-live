import { useEffect, useRef } from "react";
import { Link } from "react-router";
import styles from "./LessonPage.module.css";

export function CourseCompleteDialog({ courseTitle, onClose }) {
  const dialog = useRef(null);
  useEffect(() => {
    if (!dialog.current.open) dialog.current.showModal();
  }, []);

  return (
    <dialog ref={dialog} className={styles.dialog} onClose={onClose}>
      <p className={styles.trophy} aria-hidden>
        🎓
      </p>
      <h2>Congratulations!</h2>
      <p>
        You finished <strong>{courseTitle}</strong> and earned your free certificate. It is being
        prepared now and will appear on your dashboard, ready to add to LinkedIn.
      </p>
      <div className={styles.dialogActions}>
        <Link to="/dashboard" className="btn btn-primary">
          See my certificate
        </Link>
        <button className="btn btn-outline" onClick={() => dialog.current.close()}>
          Close
        </button>
      </div>
    </dialog>
  );
}
