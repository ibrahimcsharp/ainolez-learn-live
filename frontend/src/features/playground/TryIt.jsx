import { lazy, Suspense, useEffect, useState } from "react";
import { API_ORIGIN } from "../../shared/api/client";
import { useAssistant } from "../assistant/AssistantProvider";
import { IFRAME_LANGUAGES, iframeDocument, runCode } from "./runners";
import styles from "./TryIt.module.css";

const CodeEditor = lazy(() => import("./CodeEditor"));

/**
 * W3Schools-style "Try it Yourself": edit the code, press Run, see the result.
 * `children(code, result)` can add buttons (an exercise's Submit) under the editor.
 */
export function TryIt({ language, starterCode, children }) {
  const [code, setCode] = useState(starterCode);
  const [result, setResult] = useState(null);
  const [running, setRunning] = useState(false);
  const assistant = useAssistant();

  async function run() {
    if (IFRAME_LANGUAGES.has(language)) {
      // IframeOutput runs this snapshot, so typing afterwards does not restart it.
      setResult({ runId: crypto.randomUUID(), code, output: "" });
      return;
    }
    setRunning(true);
    setResult(null);
    try {
      setResult(await runCode(language, code));
    } catch (error) {
      setResult({ output: "", error: error.message });
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className={styles.tryit}>
      <div className={styles.editor}>
        <Suspense fallback={<textarea className={styles.fallback} value={code} readOnly />}>
          <CodeEditor value={code} onChange={setCode} language={language} />
        </Suspense>
      </div>
      <div className={styles.toolbar}>
        <button className="btn btn-primary" onClick={run} disabled={running}>
          {running ? (language === "python" ? "Starting Python…" : "Running…") : "Run ❯"}
        </button>
        <button className="btn btn-outline" onClick={() => setCode(starterCode)}>
          Reset
        </button>
        {children?.(code, result)}
        {assistant?.config?.enabled && (
          <button className="btn btn-outline" onClick={() => assistant.ask(askAbout(result), { code, language })}>
            ✨ Ask AI
          </button>
        )}
      </div>
      {result && <Output language={language} result={result} onLogs={setResult} />}
    </div>
  );
}

function Output({ language, result, onLogs }) {
  if (IFRAME_LANGUAGES.has(language)) {
    return (
      <IframeOutput key={result.runId} language={language} code={result.code}
        runId={result.runId} onLogs={onLogs} />
    );
  }
  return (
    <div className={styles.output} aria-live="polite">
      {result.tables?.map((table, i) => (
        <table key={i} className={styles.table}>
          <thead>
            <tr>{table.columns.map((c) => <th key={c}>{c}</th>)}</tr>
          </thead>
          <tbody>
            {table.values.map((row, r) => (
              <tr key={r}>{row.map((cell, c) => <td key={c}>{String(cell)}</td>)}</tr>
            ))}
          </tbody>
        </table>
      ))}
      {!result.tables && (
        <pre>{result.output || (result.error || result.images?.length ? "" : "(no output)")}</pre>
      )}
      {result.images?.map((image, i) => (
        <img key={i} className={styles.chart} src={`data:image/png;base64,${image}`} alt={`Chart ${i + 1}`} />
      ))}
      {result.error && <pre className={styles.error}>{result.error}</pre>}
    </div>
  );
}

/**
 * The sandbox: the code runs in a sandboxed iframe of the API's /runner/ page (another
 * origin), so it cannot reach this page, its cookies or storage.
 */
function IframeOutput({ language, code, runId, onLogs }) {
  const [logs, setLogs] = useState([]);
  const send = (event) =>
    event.currentTarget.contentWindow.postMessage(
      { source: "ainolez-run", html: iframeDocument(language, code, runId) },
      "*", // a sandboxed frame has no origin to name
    );

  useEffect(() => {
    function receive(event) {
      if (event.data?.source === "ainolez" && event.data.runId === runId) {
        setLogs((previous) => [...previous, event.data.text]);
      }
    }
    window.addEventListener("message", receive);
    return () => window.removeEventListener("message", receive);
  }, [runId]);

  useEffect(() => {
    onLogs((previous) => ({ ...previous, output: logs.join("\n") }));
  }, [logs, onLogs]);

  return (
    <div className={styles.output}>
      <iframe title="Result" className={styles.frame} sandbox="allow-scripts allow-modals"
        src={`${API_ORIGIN}/runner/`} onLoad={send} />
      {logs.length > 0 && <pre>{logs.join("\n")}</pre>}
    </div>
  );
}

function askAbout(result) {
  if (result?.error) return `My code shows this error: ${result.error}. What is wrong?`;
  return "Explain this code step by step. How could I improve it?";
}
