import { ExternalLink, Plus } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { useApi } from "../../../shared/hooks/useApi";
import { RecordActions, StatusBadge } from "../shared/RecordActions";
import styles from "../shared/admin.module.css";

export const PAGES = "/admin/website/pages";

/** Admin -> Pages: About, Privacy and other pages that are not courses. */
export function PagesPage() {
  const [query, setQuery] = useState("");
  const list = useApi(`${PAGES}/?page_size=500&q=${encodeURIComponent(query)}`);
  const navigate = useNavigate();
  const rows = list.data?.results ?? [];

  return (
    <>
      <div className={styles.toolbar}>
        <h1>Pages</h1>
        <input type="search" placeholder="Search pages" value={query} onChange={(e) => setQuery(e.target.value)} />
        <Link className="btn btn-primary" to="/admin/pages/new">
          <Plus /> New page
        </Link>
      </div>
      {list.data && !rows.length && (
        <div className={`card ${styles.empty}`}>
          <h3>{query ? "No page matches your search." : "No pages yet"}</h3>
          <p className="muted">
            Pages are for About, Contact, Privacy and similar text, or your own HTML, CSS and JavaScript (a
            custom code page). Each one gets its own address, like /about,
            and you can link it from the header or footer in <Link to="/admin/menus">Menus</Link>.
          </p>
        </div>
      )}
      {rows.length > 0 && (
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Page</th>
              <th>Updated</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id}>
                <td>
                  <Link to={`/admin/pages/${row.id}`}>{row.title}</Link> <StatusBadge row={row} />
                  {row.kind === "code" && <span className={styles.badge}>Custom code</span>}
                  <div className="muted">/{row.slug}</div>
                </td>
                <td className="muted">{new Date(row.updated_at).toLocaleDateString()}</td>
                <td>
                  <RecordActions base={PAGES} row={row} onChange={list.reload}
                    onEdit={() => navigate(`/admin/pages/${row.id}`)}>
                    {row.is_active && (
                      <a className={`btn btn-outline ${styles.small}`} href={`/${row.slug}`} target="_blank"
                        rel="noreferrer">
                        <ExternalLink /> View
                      </a>
                    )}
                  </RecordActions>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
