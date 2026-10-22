import { NotFound } from "../../app/NotFound";
import { useApi } from "../../shared/hooks/useApi";
import { PageLoader } from "../../shared/ui/Loader";
import { CodePageFrame } from "./CodePageFrame";
import styles from "./SitePage.module.css";

/** A page made in Admin -> Pages, shown at /<slug>: written text or custom code. */
export function SitePage({ slug }) {
  const { data: page, error } = useApi(`/public/site/pages/${slug}/`);
  if (error?.status === 404) return <NotFound />;
  if (error) return <p className="page-loading">{error.message}</p>;
  if (!page) return <PageLoader />;
  if (page.kind === "code") return <CodePageFrame key={page.frame_path} page={page} />;
  return (
    <article className={`container page-body ${styles.page}`}>
      <h1>{page.title}</h1>
      {/* Sanitised by the API (nh3) when the page was saved. */}
      <div className="lesson-content" dangerouslySetInnerHTML={{ __html: page.content_html }} />
    </article>
  );
}
