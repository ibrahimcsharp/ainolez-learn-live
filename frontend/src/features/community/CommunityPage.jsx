import { useState } from "react";
import { Link, useSearchParams } from "react-router";
import { useAuth } from "../../app/AuthProvider";
import { api } from "../../shared/api/client";
import { useApi } from "../../shared/hooks/useApi";
import { useFormFields, useSubmit } from "../../shared/hooks/useForm";
import { Field, FormError } from "../../shared/ui/Field";
import styles from "./Community.module.css";

export function CommunityPage() {
  const [params, setParams] = useSearchParams();
  const space = params.get("space") ?? "";
  const query = params.get("q") ?? "";
  const spaces = useApi("/community/spaces/");
  const posts = useApi(`/community/posts/?space=${space}&q=${encodeURIComponent(query)}`);
  const { user } = useAuth();
  const [writing, setWriting] = useState(false);

  return (
    <div className={`container ${styles.layout}`}>
      <aside className={styles.spaces}>
        <h3>Spaces</h3>
        <button aria-pressed={!space} onClick={() => setParams({})}>All posts</button>
        {(spaces.data ?? []).map((s) => (
          <button key={s.slug} aria-pressed={space === s.slug} onClick={() => setParams({ space: s.slug })}>
            {s.icon} {s.name} <span className="muted">{s.post_count}</span>
          </button>
        ))}
      </aside>
      <main>
        <div className={styles.toolbar}>
          <h1>Community</h1>
          <form onSubmit={(e) => { e.preventDefault(); setParams({ ...(space && { space }), q: e.target.q.value }); }}>
            <input name="q" type="search" defaultValue={query} placeholder="Search posts" className={styles.search} />
          </form>
          {user ? (
            <button className="btn btn-primary" onClick={() => setWriting(true)}>New post</button>
          ) : (
            <Link to="/login" className="btn btn-outline">Log in to post</Link>
          )}
        </div>
        {writing && (
          <NewPost spaces={spaces.data ?? []} defaultSpace={space}
            onDone={() => { setWriting(false); posts.reload(); }} onCancel={() => setWriting(false)} />
        )}
        {posts.data?.length === 0 && <p className="card">No posts here yet. Start the conversation!</p>}
        {(posts.data ?? []).map((post) => (
          <Link key={post.id} to={`/community/posts/${post.id}`} className={`card ${styles.postRow}`}>
            <div>
              <h3>{post.is_pinned && "📌 "}{post.title}</h3>
              <p className={styles.meta}>
                {post.space.icon} {post.space.name} · {post.author} · {new Date(post.created_at).toLocaleDateString()}
              </p>
            </div>
            <span className={styles.counts}>💬 {post.reply_count} · ♥ {post.likes}</span>
          </Link>
        ))}
      </main>
    </div>
  );
}

function NewPost({ spaces, defaultSpace, onDone, onCancel }) {
  const first = spaces.find((s) => s.slug === defaultSpace) ?? spaces[0];
  const [form, onChange] = useFormFields({ space: first?.id ?? "", title: "", body_md: "" });
  const [notice, setNotice] = useState(null);
  const { submit, busy, error } = useSubmit(async () => {
    const data = await api("/community/posts/", { method: "POST", body: form });
    if (data.status === "approved") onDone();
    else setNotice(data.detail);
  });

  if (notice) {
    return (
      <div className="card notice notice-success">
        {notice} <button className="btn btn-outline" onClick={onDone}>OK</button>
      </div>
    );
  }
  return (
    <form className="card" onSubmit={submit} style={{ marginBottom: 16 }}>
      <FormError error={error} />
      <Field label="Space" name="space" as="select" value={form.space} onChange={onChange} error={error}>
        {spaces.map((s) => <option key={s.id} value={s.id}>{s.icon} {s.name}</option>)}
      </Field>
      <Field label="Title" name="title" required maxLength={200} value={form.title} onChange={onChange} error={error} />
      <Field label="Your post (Markdown and ```code``` work)" name="body_md" as="textarea" rows={6} required
        value={form.body_md} onChange={onChange} error={error} />
      <button className="btn btn-primary" disabled={busy}>Post</button>{" "}
      <button type="button" className="btn btn-outline" onClick={onCancel}>Cancel</button>
    </form>
  );
}
