import { copyFileSync } from "node:fs";
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// dist/shell.html is the untouched app page. The server's SEO build fills a copy
// of it for every public page; Apache serves it for all other paths.
const spaShell = {
  name: "spa-shell",
  apply: "build",
  closeBundle() {
    copyFileSync("dist/index.html", "dist/shell.html");
  },
};

// Content-Security-Policy of the built site. Learner code runs on the API's
// /runner/ page (another origin), so scripts here can stay strict.
// Keep frame-src in step with ALLOWED_IFRAME_HOSTS in backend content_tools/embeds.py.
function contentSecurityPolicy(apiUrl) {
  const api = apiUrl?.startsWith("http") ? new URL(apiUrl).origin : "";
  const cdn = "https://cdn.jsdelivr.net"; // Pyodide and sql.js
  const frames = [
    "https://www.youtube-nocookie.com", "https://player.vimeo.com", "https://www.loom.com",
    "https://drive.google.com", "https://docs.google.com", "https://codepen.io", "https://replit.com",
  ];
  const policy = [
    "default-src 'self'",
    `script-src 'self' 'wasm-unsafe-eval' ${cdn}`,
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data: blob: https:",
    "media-src 'self' https:",
    `connect-src 'self' ${api} ${cdn}`,
    `frame-src 'self' ${api} ${frames.join(" ")}`,
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
  ];
  return {
    name: "csp",
    apply: "build",
    transformIndexHtml: (html) =>
      html.replace("<head>", `<head>\n    <meta http-equiv="Content-Security-Policy" content="${policy.join("; ")}" />`),
  };
}

export default defineConfig(({ mode }) => ({
  plugins: [react(), contentSecurityPolicy(loadEnv(mode, process.cwd()).VITE_API_URL), spaShell],
  server: {
    // Locally the API runs on Django's dev server; the proxy keeps it same-origin.
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/media": "http://127.0.0.1:8000",
      "/share": "http://127.0.0.1:8000",
      "/runner": "http://127.0.0.1:8000",
    },
  },
  preview: {
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/media": "http://127.0.0.1:8000",
      "/runner": "http://127.0.0.1:8000",
    },
  },
  test: {
    environment: "jsdom",
  },
}));
