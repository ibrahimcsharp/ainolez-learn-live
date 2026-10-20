import { useEffect, useState } from "react";
import { api } from "../api/client";

/** GET `path` (skipped when null). `reload()` fetches it again. */
export function useApi(path) {
  const [state, setState] = useState({ data: null, error: null, loading: Boolean(path) });
  const [version, setVersion] = useState(0);

  useEffect(() => {
    if (!path) return undefined;
    let live = true;
    setState((previous) => ({ ...previous, loading: true }));
    api(path)
      .then((data) => live && setState({ data, error: null, loading: false }))
      .catch((error) => live && setState({ data: null, error, loading: false }));
    return () => {
      live = false;
    };
  }, [path, version]);

  return { ...state, reload: () => setVersion((v) => v + 1) };
}
