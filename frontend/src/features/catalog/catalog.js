import { useEffect, useState } from "react";
import { api } from "../../shared/api/client";

/*
 * The /courses data: { categories, courses (with lesson_count), paths }.
 * api() reads the SEO build's static copy first (see client.js). The copy from the last
 * visit is shown first, so a repeat visit draws at once. Loaded once per visit.
 */
const KEY = "ainolez.catalog";

let current = saved();
let loading = null;

function load() {
  loading ??= api("/public/catalog/")
    .then((data) => {
      current = data;
      try {
        localStorage.setItem(KEY, JSON.stringify(data));
      } catch {
        // storage full or blocked: this visit still has the data
      }
      return { data, error: null };
    })
    .catch((error) => {
      loading = null; // let "Try again" ask once more
      return { data: current, error };
    });
  return loading;
}

/** { data, loading, error, retry }. `data` may be last visit's copy while `loading`. */
export function useCatalog() {
  const [state, setState] = useState({ data: current, error: null, loading: true });
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let live = true;
    load().then((result) => live && setState({ ...result, loading: false }));
    return () => {
      live = false;
    };
  }, [attempt]);
  const retry = () => {
    setState((previous) => ({ ...previous, error: null, loading: true }));
    setAttempt((n) => n + 1);
  };
  return { ...state, retry };
}

function saved() {
  try {
    const data = JSON.parse(localStorage.getItem(KEY));
    return isCatalog(data) ? data : null;
  } catch {
    return null;
  }
}

function isCatalog(data) {
  return Array.isArray(data?.courses) && Array.isArray(data?.categories) && Array.isArray(data?.paths);
}
