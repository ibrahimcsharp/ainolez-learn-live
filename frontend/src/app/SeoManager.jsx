import { useEffect } from "react";
import { useLocation } from "react-router";
import { api } from "../shared/api/client";

/**
 * Puts each page's title, meta tags and JSON-LD into <head>. The values come
 * from the server (Admin -> SEO), the same ones the prerendered HTML has.
 */
export function SeoManager() {
  const { pathname } = useLocation();

  useEffect(() => {
    let live = true;
    api(`/public/seo/?path=${encodeURIComponent(pathname)}`)
      .then((seo) => live && applySeo(seo))
      .catch(() => {}); // keep the previous tags if the API is unreachable
    return () => {
      live = false;
    };
  }, [pathname]);

  return null;
}

function applySeo({ title, tags, json_ld: jsonLd }) {
  document.title = title;
  document.head.querySelectorAll("[data-seo]").forEach((element) => element.remove());
  for (const { tag, ...attributes } of tags) {
    const element = document.createElement(tag);
    Object.entries(attributes).forEach(([name, value]) => element.setAttribute(name, value));
    add(element);
  }
  for (const data of jsonLd) {
    const script = document.createElement("script");
    script.type = "application/ld+json";
    script.textContent = JSON.stringify(data);
    add(script);
  }
}

function add(element) {
  element.setAttribute("data-seo", "");
  document.head.append(element);
}
