import { useEffect, useState } from "react";
import { api } from "../../../shared/api/client";

/** Server-rendered HTML for `markdown`, refreshed 400 ms after typing stops. */
export function useMarkdownPreview(markdown) {
  const [html, setHtml] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      api("/admin/content-tools/md-convert/", { method: "POST", body: { markdown } })
        .then((data) => setHtml(data.html))
        .catch(() => {});
    }, 400);
    return () => clearTimeout(timer);
  }, [markdown]);

  return html;
}
