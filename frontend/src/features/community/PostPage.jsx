import { useState } from "react";
import { Link, useParams } from "react-router";
import { useAuth } from "../../app/AuthProvider";
import { NotFound } from "../../app/NotFound";
import { api } from "../../shared/api/client";
import { useApi } from "../../shared/hooks/useApi";
import { useSubmit } from "../../shared/hooks/useForm";
import { FormError } from "../../shared/ui/Field";
import { LikeButton, ReportButton } from "./Actions";
import styles from "./Community.module.css";

export function PostPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const post = useApi(`/community/posts/${id}/`);
  if (post.error?.status === 404) return <NotFound />;
  if (!post.data) return <p className="page-loading is-loading">Loading…</p>;
  const data = post.data;

  async function accept(replyId) {
    await api(`/community/replies/${replyId}/accept/`, { method: "POST" });
    post.reload();
  }

  return (
    <div className="container page-body" style={{ maxWidth: "calc(820px + 2 * var(--gutter))" }}>
      <p>
        <Link to={`/community?space=${data.space.slug}`}>← {data.space.icon} {data.space.name}</Link>
      </p>
      <article className="card">
        <h1>{data.is_pinned && "📌 "}{data.title}</h1>
        <p className={styles.meta}>
          {data.author} · {new Date(data.created_at).toLocaleString()}
          {data.status === "pending" && <span className={styles.pending}> waiting for approval</span>}
        </p>
        <div className="lesson-content" dangerouslySetInnerHTML={{ __html: data.body_html }} />
        {user && data.status === "approved" && (
          <p className={styles.actions}>
            <LikeButton targetType="post" targetId={data.id} liked={data.liked} count={data.likes} />
            <ReportButton targetType="post" targetId={data.id} />
          </p>
        )}
      </article>

      <h2 style={{ marginTop: 28 }}>{data.reply_count} {data.reply_count === 1 ? "reply" : "replies"}</h2>
      {data.replies.map((reply) => (
        <article key={reply.id} className={`card ${styles.reply} ${reply.is_helpful ? styles.helpful : ""}`}>
          <p className={styles.meta}>
            <strong>{reply.author}</strong> · {new Date(reply.created_at).toLocaleString()}
            {reply.is_helpful && <strong className={styles.accepted}> ✓ Helpful answer</strong>}
            {reply.status === "pending" && <span className={styles.pending}> waiting for approval</span>}
          </p>
          <div className="lesson-content" dangerouslySetInnerHTML={{ __html: reply.body_html }} />
          {user && reply.status === "approved" && (
            <p className={styles.actions}>
              <LikeButton targetType="reply" targetId={reply.id} liked={reply.liked} count={reply.likes} />
              <ReportButton targetType="reply" targetId={reply.id} />
              {data.is_mine && !reply.is_helpful && (
                <button className={styles.action} onClick={() => accept(reply.id)}>Mark as helpful</button>
              )}
            </p>
          )}
        </article>
      ))}

      {data.is_locked ? (
        <p className="notice notice-info">This post is locked for new replies.</p>
      ) : user ? (
        <ReplyForm postId={data.id} onDone={post.reload} />
      ) : (
        <p><Link to="/login">Log in</Link> to reply.</p>
      )}
    </div>
  );
}

function ReplyForm({ postId, onDone }) {
  const [body, setBody] = useState("");
  const [notice, setNotice] = useState(null);
  const { submit, busy, error } = useSubmit(async () => {
    const data = await api(`/community/posts/${postId}/replies/`, { method: "POST", body: { body_md: body } });
    setBody("");
    setNotice(data.status === "approved" ? null : data.detail);
    onDone();
  });
  return (
    <form onSubmit={submit} style={{ marginTop: 16 }}>
      <FormError error={error} />
      {notice && <p className="notice notice-success">{notice}</p>}
      <textarea className={styles.textarea} rows={4} value={body} onChange={(e) => setBody(e.target.value)}
        placeholder="Write a helpful reply (Markdown works)" required />
      <button className="btn btn-primary" disabled={busy}>Reply</button>
    </form>
  );
}
