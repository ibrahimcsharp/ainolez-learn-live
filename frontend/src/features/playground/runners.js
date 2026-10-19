/*
 * Runs learners' code in the browser, never on the server.
 *   html / css / javascript -> a sandboxed iframe (see IframeOutput)
 *   python                  -> Pyodide (CPython compiled to WebAssembly)
 *   sql                     -> sql.js (SQLite compiled to WebAssembly)
 * Pyodide and sql.js are large, so they load from the CDN the first time only.
 */
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
const SQLJS_URL = "https://cdn.jsdelivr.net/npm/sql.js@1.12.0/dist/";

export const IFRAME_LANGUAGES = new Set(["html", "css", "javascript"]);

/** Python or SQL -> { output, tables?, error? } */
export async function runCode(language, code) {
  if (language === "python") return runPython(code);
  if (language === "sql") return runSql(code);
  throw new Error(`No runner for ${language}`);
}

/**
 * The page shown in the iframe. console.log and errors are sent to the parent
 * with postMessage, tagged with runId, so exercises can check the output.
 */
export function iframeDocument(language, code, runId) {
  const relay = `<script>
    (function () {
      function send(text) { parent.postMessage({ source: "ainolez", runId: ${JSON.stringify(runId)}, text: text }, "*"); }
      var log = console.log;
      console.log = function () {
        var text = Array.prototype.map.call(arguments, function (a) {
          return typeof a === "object" ? JSON.stringify(a) : String(a);
        }).join(" ");
        send(text); log.apply(console, arguments);
      };
      window.onerror = function (message) { send("Error: " + message); };
    })();
  </script>`;
  if (language === "javascript") {
    return `<!doctype html><html><body style="font-family:monospace">${relay}<script>${code.replace(/<\/script/gi, "<\\/script")}</script></body></html>`;
  }
  return `${relay}${code}`; // html and css examples are whole HTML documents
}

// matplotlib cannot open windows in the browser: charts are drawn to PNG and shown under the output.
const CHARTS_SETUP = `
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
plt.show = lambda *args, **kwargs: None
plt.close("all")
`;
const CHARTS_COLLECT = `
import base64, io
import matplotlib.pyplot as plt
images = []
for number in plt.get_fignums():
    buffer = io.BytesIO()
    plt.figure(number).savefig(buffer, format="png", bbox_inches="tight", dpi=100)
    images.append(base64.b64encode(buffer.getvalue()).decode())
plt.close("all")
images
`;

let pyodideReady;
async function runPython(code) {
  pyodideReady ??= loadScript(`${PYODIDE_URL}pyodide.js`).then(() =>
    window.loadPyodide({ indexURL: PYODIDE_URL }),
  );
  const pyodide = await pyodideReady;
  const lines = [];
  pyodide.setStdout({ batched: (text) => lines.push(text) });
  pyodide.setStderr({ batched: (text) => lines.push(text) });
  const scope = pyodide.globals.get("dict")(); // a fresh namespace for every run
  try {
    await pyodide.loadPackagesFromImports(code); // numpy, pandas, scikit-learn... (first use only)
    const charts = code.includes("matplotlib");
    if (charts) pyodide.runPython(CHARTS_SETUP);
    await pyodide.runPythonAsync(code, { globals: scope });
    return { output: lines.join("\n"), images: charts ? pyodide.runPython(CHARTS_COLLECT).toJs() : [] };
  } catch (error) {
    const last = String(error.message).trim().split("\n").pop(); // e.g. "NameError: name 'x' ..."
    return { output: lines.join("\n"), error: last };
  } finally {
    scope.destroy();
  }
}

let sqlReady;
async function runSql(code) {
  sqlReady ??= loadScript(`${SQLJS_URL}sql-wasm.js`).then(() =>
    window.initSqlJs({ locateFile: (file) => SQLJS_URL + file }),
  );
  const SQL = await sqlReady;
  const db = new SQL.Database(); // empty database every run: examples create their tables
  try {
    const tables = db.exec(code);
    const output = tables
      .map((t) => [t.columns.join("\t"), ...t.values.map((row) => row.join("\t"))].join("\n"))
      .join("\n\n");
    return { output, tables };
  } catch (error) {
    return { output: "", error: String(error.message) };
  } finally {
    db.close();
  }
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`Could not load ${src}`));
    document.head.append(script);
  });
}
