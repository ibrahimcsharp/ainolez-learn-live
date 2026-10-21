import { useEffect, useState } from "react";
import { api } from "../../shared/api/client";

/*
 * The header and footer menus (Admin -> Menus) are drawn on first paint:
 *   1. the prerendered page carries them in <script id="site-menus"> (seo_build),
 *   2. otherwise the copy saved by the last visit is used,
 * and the API is asked straight away, at start-up, so changes show up quickly.
 */
const KEY = "ainolez.menus";
const EMPTY = { header: [], footer: [] };

let current = embedded() ?? saved() ?? EMPTY;
const listeners = new Set();
export const ready = api("/public/site/menus/")
  .then((menus) => {
    current = menus;
    try {
      localStorage.setItem(KEY, JSON.stringify(menus));
    } catch {
      // storage full or blocked: the embedded copy still works
    }
    listeners.forEach((listener) => listener(menus));
  })
  .catch(() => {}); // keep what we have if the API is unreachable

/** { header: [link], footer: [{ id, name, items: [link] }] } */
export function useMenus() {
  const [menus, setMenus] = useState(current);
  useEffect(() => {
    listeners.add(setMenus);
    setMenus(current); // in case the API answered before this mounted
    return () => listeners.delete(setMenus);
  }, []);
  return menus;
}

function embedded() {
  return parse(document.getElementById("site-menus")?.textContent);
}

function saved() {
  try {
    return parse(localStorage.getItem(KEY));
  } catch {
    return null;
  }
}

function parse(text) {
  try {
    const menus = text && JSON.parse(text);
    return Array.isArray(menus?.header) && Array.isArray(menus?.footer) ? menus : null;
  } catch {
    return null;
  }
}
