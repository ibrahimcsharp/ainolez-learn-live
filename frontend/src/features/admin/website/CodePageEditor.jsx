import {
  Columns2,
  FileCode2,
  FileUp,
  Maximize2,
  Minimize2,
  Monitor,
  RefreshCw,
  Rows2,
  ShieldAlert,
  Smartphone,
  Tablet,
  Terminal,
  Trash2,
  Wand2,
} from "lucide-react";
import { lazy, Suspense, useEffect, useMemo, useRef, useState } from "react";
import { API_ORIGIN } from "../../../shared/api/client";
import { LoadingBar, Spinner } from "../../../shared/ui/Loader";
import { isWholeDocument, pageDocument, tabForFile, TEMPLATES } from "./codePage";
import styles from "./CodePageEditor.module.css";

const CodeEditor = lazy(() => import("../../playground/CodeEditor"));

const FILES = [
  { name: "code_html", file: "index.html", language: "html", dot: "#e44d26" },
  { name: "code_css", file: "style.css", language: "stylesheet", dot: "#2965f1" },
  { name: "code_js", file: "script.js", language: "javascript", dot: "#f0db4f" },
];
const DEVICES = [
  { key: "desktop", label: "Desktop", icon: Monitor, width: null },
  { key: "tablet", label: "Tablet", icon: Tablet, width: 768 },
  { key: "phone", label: "Phone", icon: Smartphone, width: 375 },
];
const DELAY_MS = 600; // wait for a pause in typing before the preview reloads
// No word from the preview this long after its frame loads (or at all): something blocked it.
const BLOCKED_AFTER_LOAD_MS = 4000;
const BLOCKED_AFTER_START_MS = 12000;

/**
 * The editor of a custom code page: HTML, CSS and JS tabs, a live preview (in the
 * API's sandboxed /runner/ page, like Try-it) with phone and tablet sizes, a console
 * that shows the page's logs and errors, file import, templates and full screen.
 * `values` holds code_html, code_css and code_js; `onCode(name, text)` changes one.
 */
export function CodePageEditor({ title, values, onCode, onSave }) {
  const [tab, setTab] = useState("code_html");
  const [layout, setLayout] = useState("split"); // split | stacked
  const [full, setFull] = useState(false);
  const [device, setDevice] = useState("desktop");
  const [auto, setAuto] = useState(true);
  const [logs, setLogs] = useState([]);
  const [showConsole, setShowConsole] = useState(false);
  const [run, setRun] = useState(() => ({ id: crypto.randomUUID(), code: pick(values) }));
  const [loading, setLoading] = useState(true);
  const [heard, setHeard] = useState(null); // the run id the preview answered for
  const [blocked, setBlocked] = useState(false);
  const files = useRef(null);

  const code = pick(values);
  const stale = code.html !== run.code.html || code.css !== run.code.css || code.js !== run.code.js;

  function refresh() {
    setLogs([]);
    setLoading(true);
    setBlocked(false);
    setRun({ id: crypto.randomUUID(), code: pick(values) });
  }

  // Live preview: reload after a pause in typing.
  const later = useRef(refresh);
  later.current = refresh;
  useEffect(() => {
    if (!auto || !stale) return undefined;
    const timer = setTimeout(() => later.current(), DELAY_MS);
    return () => clearTimeout(timer);
  }, [auto, stale, code.html, code.css, code.js]);

  // Console lines and link clicks from the preview.
  useEffect(() => {
    function receive(event) {
      const data = event.data;
      if (data?.source !== "ainolez-preview" || data.runId !== run.id) return;
      setHeard(run.id);
      setBlocked(false);
      if (data.type === "ready") return;
      const text = data.type === "link" ? `Link clicked: ${data.text} (opens on the site)` : String(data.text);
      setLogs((previous) => [...previous.slice(-199), { type: data.type, text }]);
      if (data.type === "error") setShowConsole(true);
    }
    window.addEventListener("message", receive);
    return () => window.removeEventListener("message", receive);
  }, [run.id]);

  // A preview that never answers was blocked (often by a browser extension).
  useEffect(() => {
    if (heard === run.id) return undefined;
    const timer = setTimeout(() => setBlocked(true), loading ? BLOCKED_AFTER_START_MS : BLOCKED_AFTER_LOAD_MS);
    return () => clearTimeout(timer);
  }, [heard, run.id, loading]);

  // Full screen: Escape leaves it, and the page behind does not scroll.
  useEffect(() => {
    if (!full) return undefined;
    const key = (event) => event.key === "Escape" && setFull(false);
    document.addEventListener("keydown", key);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", key);
      document.body.style.overflow = "";
    };
  }, [full]);

  function keys(event) {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
      event.preventDefault();
      onSave?.();
    } else if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault();
      refresh();
    }
  }

  function applyTemplate(key) {
    if (!key) return;
    const hasCode = FILES.some((f) => (values[f.name] ?? "").trim());
    if (hasCode && !window.confirm("Replace the code in all three tabs with this template?")) return;
    const template = TEMPLATES[key];
    FILES.forEach((f) => onCode(f.name, template[f.name]));
    setTab("code_html");
  }

  async function importFiles(event) {
    const chosen = [...event.target.files];
    event.target.value = "";
    const skipped = [];
    for (const file of chosen) {
      const name = tabForFile(file.name);
      if (!name) {
        skipped.push(file.name);
        continue;
      }
      if ((values[name] ?? "").trim() && !window.confirm(`Replace the code in ${fileOf(name).file} with ${file.name}?`)) {
        continue;
      }
      onCode(name, await file.text());
      setTab(name);
    }
    if (skipped.length) window.alert(`Only .html, .css and .js files can be imported. Skipped: ${skipped.join(", ")}`);
  }

  const width = DEVICES.find((d) => d.key === device).width;
  const errors = logs.filter((line) => line.type === "error").length;
  const current = fileOf(tab);
  const whole = isWholeDocument(values.code_html);

  return (
    <div className={`${styles.workbench} ${full ? styles.full : ""}`} data-layout={layout} onKeyDown={keys}>
      <div className={styles.bar}>
        <div className={styles.tabs} role="tablist" aria-label="Code files">
          {FILES.map((f) => (
            <button key={f.name} type="button" role="tab" aria-selected={tab === f.name} className={styles.tab}
              onClick={() => setTab(f.name)}>
              <span className={styles.dot} style={{ background: f.dot }} />
              {f.file}
              <span className={styles.count}>{lines(values[f.name])}</span>
            </button>
          ))}
        </div>
        <div className={styles.tools}>
          <label className={styles.tool} title="Start from a template">
            <Wand2 size={16} />
            <select value="" onChange={(e) => applyTemplate(e.target.value)} aria-label="Start from a template">
              <option value="">Template…</option>
              {Object.entries(TEMPLATES).map(([key, t]) => <option key={key} value={key}>{t.label}</option>)}
            </select>
          </label>
          <button type="button" className={styles.tool} onClick={() => files.current.click()}
            title="Import .html, .css and .js files">
            <FileUp size={16} /> <span className={styles.wide}>Import</span>
          </button>
          <input ref={files} type="file" hidden multiple accept=".html,.htm,.css,.js,.mjs" onChange={importFiles} />
          <span className={styles.sep} />
          <button type="button" className={styles.icon} aria-pressed={layout === "split"} title="Side by side"
            onClick={() => setLayout("split")}>
            <Columns2 size={16} />
          </button>
          <button type="button" className={styles.icon} aria-pressed={layout === "stacked"} title="Preview below"
            onClick={() => setLayout("stacked")}>
            <Rows2 size={16} />
          </button>
          <button type="button" className={styles.icon} onClick={() => setFull(!full)}
            title={full ? "Leave full screen (Esc)" : "Full screen"} aria-pressed={full}>
            {full ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
          </button>
        </div>
      </div>

      <div className={styles.panes}>
        <div className={styles.code}>
          <Suspense fallback={<div className={styles.codeLoading}><Spinner size={28} label="Loading the editor" /></div>}>
            <CodeEditor key={tab} language={current.language} value={values[tab] ?? ""}
              onChange={(text) => onCode(tab, text)} />
          </Suspense>
          <div className={styles.status}>
            <FileCode2 size={14} />
            {tab === "code_html"
              ? whole
                ? "Whole document: kept as written; style.css goes in <head>, script.js before </body>."
                : "Page content: the site wraps it in <html>, <head> and <body>."
              : tab === "code_css"
                ? "Added in a <style> tag in the page's <head>."
                : "Runs after the HTML, at the end of <body>."}
            <span className={styles.keys}>Ctrl+S save · Ctrl+Enter refresh</span>
          </div>
        </div>

        <div className={styles.preview}>
          <div className={styles.previewBar}>
            <span className={styles.previewTitle}>Preview</span>
            <div className={styles.devices} role="group" aria-label="Preview size">
              {DEVICES.map(({ key, label, icon: Icon }) => (
                <button key={key} type="button" className={styles.icon} aria-pressed={device === key} title={label}
                  onClick={() => setDevice(key)}>
                  <Icon size={16} />
                </button>
              ))}
            </div>
            <label className={styles.auto}>
              <input type="checkbox" checked={auto} onChange={(e) => setAuto(e.target.checked)} /> Live
            </label>
            <button type="button" className={styles.tool} onClick={refresh} title="Refresh (Ctrl+Enter)">
              <RefreshCw size={15} className={loading ? styles.turning : undefined} />
              {stale && !auto && <span className={styles.changed}>changed</span>}
            </button>
            <button type="button" className={`${styles.tool} ${errors ? styles.hasErrors : ""}`}
              aria-pressed={showConsole} onClick={() => setShowConsole(!showConsole)} title="Console">
              <Terminal size={15} />
              {logs.length > 0 && <span className={styles.badge}>{errors || logs.length}</span>}
            </button>
          </div>
          <div className={styles.stage}>
            <div className={styles.device} style={width ? { width } : undefined} data-device={device}>
              {loading && <LoadingBar inline />}
              <PreviewFrame key={run.id} title={title} run={run} onLoaded={() => setLoading(false)} />
              {blocked && heard !== run.id && <Blocked onRetry={refresh} />}
            </div>
          </div>
          {showConsole && (
            <div className={styles.console} aria-live="polite">
              <div className={styles.consoleBar}>
                <span>Console</span>
                <button type="button" className={styles.icon} title="Clear" onClick={() => setLogs([])}>
                  <Trash2 size={14} />
                </button>
              </div>
              {logs.length === 0 && <p className={styles.empty}>console.log() and errors from the page show here.</p>}
              {logs.map((line, i) => (
                <pre key={i} className={styles.line} data-type={line.type}>{line.text}</pre>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/** Shown over the preview when it does not load. */
function Blocked({ onRetry }) {
  return (
    <div className={styles.blocked} role="alert">
      <ShieldAlert size={32} />
      <strong>The preview could not load</strong>
      <p>
        Your browser blocked it. This is usually a browser extension, such as an ad or script blocker. Allow{" "}
        <code>{new URL(API_ORIGIN).host}</code> in the extension, or open the admin in a private (Incognito) window.
      </p>
      <p className={styles.blockedNote}>Your code is not the problem, and saving still works.</p>
      <button type="button" className="btn btn-primary" onClick={onRetry}>
        <RefreshCw size={16} /> Try again
      </button>
    </div>
  );
}

/** One preview run: the runner page receives the document once it has loaded. */
function PreviewFrame({ title, run, onLoaded }) {
  const html = useMemo(
    () => pageDocument({ title, html: run.code.html, css: run.code.css, js: run.code.js, runId: run.id }),
    [title, run],
  );
  return (
    <iframe title="Page preview" className={styles.frame} src={`${API_ORIGIN}/runner/`}
      sandbox="allow-scripts allow-forms allow-modals allow-popups"
      onLoad={(event) => {
        event.currentTarget.contentWindow.postMessage({ source: "ainolez-run", html }, "*");
        setTimeout(onLoaded, 250);
      }} />
  );
}

function pick(values) {
  return { html: values.code_html ?? "", css: values.code_css ?? "", js: values.code_js ?? "" };
}

function fileOf(name) {
  return FILES.find((f) => f.name === name);
}

function lines(text) {
  return text ? text.split("\n").length : 0;
}
