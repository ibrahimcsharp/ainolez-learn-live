import { Link, useSearchParams } from "react-router";
import { useApi } from "../../shared/hooks/useApi";

export function SearchPage() {
  const query = useSearchParams()[0].get("q") ?? "";
  const { data: results, loading } = useApi(query ? `/public/search/?q=${encodeURIComponent(query)}` : null);

  return (
    <div className="container" style={{ padding: "40px 16px 64px", maxWidth: 760 }}>
      <h1>Search</h1>
      {!query && <p className="muted">Type a topic in the search box above, for example “python lists”.</p>}
      {query && loading && <p className="muted">Searching…</p>}
      {results?.length === 0 && <p>No lessons match “{query}”. Try fewer or shorter words.</p>}
      {(results ?? []).map((item) => (
        <article key={`${item.course.slug}/${item.slug}`} className="card" style={{ marginBottom: 12 }}>
          <Link to={`/${item.course.slug}/${item.slug}`}>
            <h3 style={{ margin: 0 }}>{item.title}</h3>
          </Link>
          <p className="muted" style={{ margin: "4px 0 0" }}>
            {item.course.title}
            {item.summary && ` · ${item.summary}`}
          </p>
        </article>
      ))}
    </div>
  );
}
