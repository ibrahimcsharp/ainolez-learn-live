import { useState } from "react";
import { Link } from "react-router";
import { useAuth } from "../../app/AuthProvider";
import { api } from "../../shared/api/client";
import { useApi } from "../../shared/hooks/useApi";
import { useSubmit } from "../../shared/hooks/useForm";
import { FormError } from "../../shared/ui/Field";
import { LikeButton, ReportButton } from "./Actions";
import styles from "./Community.module.css";

/** Discussion under a lesson. New comments wait for a moderator unless the author is trusted. */
export function LessonComments({ lessonId }) {
  const { user } = useAuth();
  const comments = useApi(`/community/lessons/${lessonId}/comments/`);
  const [body, setBody] = useState("");
  const [notice, setNotice] = useState(null);
  const { submit, busy, error } = useSubmit(async () => {
    const data = await api(`/community/lessons/${lessonId}/comments/`, { method: "POST", body: { body_md: body } });
    setBody("");
    setNotice(data.detail);
    comments.reload();
  });

  const rows = comments.data ?? [];
  return (
    <section className={styles.comments}>
      <h2>Discussion ({rows.filter((c) => c.status === "approved").length})</h2>
      {rows.map((comment) => (
        <article key={comment.id} className={styles.item}>
          <p className={styles.meta}>
            <strong>{comment.author}</strong> · {new Date(comment.created_at).toLocaleDateString()}
            {comment.status === "pending" && <span className={styles.pending}> waiting for approval</span>}
          </p>
          <div className="lesson-content" dangerouslySetInnerHTML={{ __html: comment.body_html }} />
          {comment.status === "approved" && user && (
            <p className={styles.actions}>
              <LikeButton targetType="comment" targetId={comment.id} liked={comment.liked} count={comment.likes} />
              <ReportButton targetType="comment" targetId={comment.id} />
            </p>
          )}
        </article>
      ))}
      {user ? (
        <form onSubmit={submit}>
          <FormError error={error} />
          {notice && <p className="notice notice-success">{notice}</p>}
          <textarea className={styles.textarea} value={body} onChange={(e) => setBody(e.target.value)} rows={3}
            placeholder="Ask a question or share a tip about this lesson (Markdown works)" required />
          <button className="btn btn-primary" disabled={busy}>
            Post comment
          </button>
        </form>
      ) : (
        <p>
          <Link to="/login">Log in</Link> to join the discussion.
        </p>
      )}
    </section>
  );
}
