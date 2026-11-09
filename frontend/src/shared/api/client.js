/*
 * Small fetch wrapper for the Django API.
 * The access token lives only in memory; the refresh token is an httpOnly cookie.
 */
const API_URL = import.meta.env.VITE_API_URL ?? "/api/v1";
/** Where the API (and the Try-it sandbox page, /runner/) lives. */
export const API_ORIGIN = new URL(API_URL, window.location.href).origin;

let accessToken = null;
let refreshing = null;
const SIGNED_IN = "ainolez.signedIn";

export class ApiError extends Error {
  constructor(status, data) {
    super(messageFrom(data) ?? "Something went wrong. Please try again.");
    this.status = status;
    this.code = data?.code;
    this.fields = data ?? {}; // DRF validation errors: { field: ["message"] }
  }
}

export function setAccessToken(token) {
  accessToken = token;
  remember(Boolean(token));
}

/** Whether this browser was signed in on its last visit; null when not known yet. */
export function signedInBefore() {
  try {
    const value = localStorage.getItem(SIGNED_IN);
    return value === null ? null : value === "1";
  } catch {
    return null;
  }
}

function remember(signedIn) {
  try {
    localStorage.setItem(SIGNED_IN, signedIn ? "1" : "0");
  } catch {
    // storage blocked: the session is checked on every visit, as before
  }
}

/*
 * The SEO build keeps static copies of public course, lesson and page data next to the
 * website (backend/modules/seo/prerender.py, write_data). The web server sends a file at
 * once, while the API first has to start Python, so public GETs read the copy first and
 * ask the API only when there is none.
 */
const STATIC = /^\/public\/(courses\/[\w-]+(?:\/lessons\/[\w-]+)?|site\/pages\/[\w-]+|site\/menus|catalog)\/$/;
const copies = new Map();

/** Where the static copy of a public GET lives, or null when it has none. */
export function staticCopy(path) {
  const match = STATIC.exec(path);
  return match ? `/data/${match[1]}.json` : null;
}

/** The static copy's data, or null when there is none. Each file is fetched once per visit. */
export function fromStatic(path) {
  const url = staticCopy(path);
  if (!url) return Promise.resolve(null);
  if (!copies.has(url)) {
    const copy = fetch(url, { cache: "no-cache" })
      .then((response) =>
        response.ok && response.headers.get("content-type")?.includes("json") ? response.json() : null,
      )
      .catch(() => null);
    copies.set(url, copy);
  }
  return copies.get(url);
}

/**
 * Call the API. `body` may be a plain object (sent as JSON) or FormData (file uploads).
 * With `raw: true` the fetch Response is returned, e.g. to download a file.
 */
export async function api(path, { method = "GET", body, raw = false, headers = {}, retry = true } = {}) {
  if (method === "GET" && !raw) {
    const copy = await fromStatic(path);
    if (copy !== null) return copy;
  }
  const isForm = body instanceof FormData;
  const response = await fetch(API_URL + path, {
    method,
    credentials: "include",
    headers: {
      ...(!isForm && { "Content-Type": "application/json" }),
      ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
      ...headers,
    },
    body: isForm ? body : body && JSON.stringify(body),
  });

  if (response.status === 401 && retry && accessToken && (await refreshAccess())) {
    return api(path, { method, body, raw, headers, retry: false }); // access token had expired
  }
  if (raw && response.ok) return response;
  const data = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) throw new ApiError(response.status, data);
  return data;
}

/** Get a new access token from the refresh cookie. Parallel callers share one request. */
export function refreshAccess() {
  refreshing ??= fetch(`${API_URL}/auth/refresh/`, { method: "POST", credentials: "include" })
    .then(async (response) => {
      accessToken = response.ok ? (await response.json()).access : null;
      remember(Boolean(accessToken));
      return Boolean(accessToken);
    })
    .catch(() => false)
    .finally(() => {
      refreshing = null;
    });
  return refreshing;
}

function messageFrom(data) {
  if (!data) return null;
  if (typeof data.detail === "string") return data.detail;
  const first = Object.values(data).flat()[0];
  return typeof first === "string" ? first : null;
}
