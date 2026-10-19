/*
 * Small fetch wrapper for the Django API.
 * The access token lives only in memory; the refresh token is an httpOnly cookie.
 */
const API_URL = import.meta.env.VITE_API_URL ?? "/api/v1";
/** Where the API (and the Try-it sandbox page, /runner/) lives. */
export const API_ORIGIN = new URL(API_URL, window.location.href).origin;

let accessToken = null;
let refreshing = null;

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
}

/**
 * Call the API. `body` may be a plain object (sent as JSON) or FormData (file uploads).
 * With `raw: true` the fetch Response is returned, e.g. to download a file.
 */
export async function api(path, { method = "GET", body, raw = false, headers = {}, retry = true } = {}) {
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
