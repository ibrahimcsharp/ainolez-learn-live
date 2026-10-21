import { NotFound } from "../../app/NotFound";
import { useApi } from "../../shared/hooks/useApi";
import styles from "./SitePage.module.css";

/** A page written in Admin -> Pages, shown at /<slug>. */
export function SitePage({ slug }) {
  const { data: page, error } = useApi(`/public/site/pages/${slug}/`);
  if (error?.status === 404) return <NotFound />;
  if (!page) return <p className="page-loading">{error ? error.message : "Loading…"}</p>;
  return (
    <article className={`container page-body ${styles.page}`}>
      <h1>{page.title}</h1>
      {/* Sanitised by the API (nh3) when the page was saved. */}
      <div className="lesson-content" dangerouslySetInnerHTML={{ __html: page.content_html }} />
    </article>
  );
}
