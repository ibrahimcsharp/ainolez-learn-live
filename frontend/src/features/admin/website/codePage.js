/*
 * Custom code pages in the admin: the preview document and the starter templates.
 * `pageDocument` follows backend website/code_page.py (what the live site serves),
 * so the preview looks the same. The preview adds a console relay on top.
 */

const BASE_CSS = "html,body{margin:0}body{font-family:Inter,'Segoe UI',Arial,sans-serif}";
const WHOLE = /^\s*(<!doctype|<html)/i;

const script = (code) => `<script>${code.replace(/<\/(script)/gi, "<\\/$1")}</script>`;
const style = (code) => `<style>${code.replace(/<\/(style)/gi, "<\\/$1")}</style>`;

/** Sends console output, errors and clicked links to the editor (tagged with runId). */
function relay(runId) {
  return `<script>
(function () {
  function send(type, text) { parent.postMessage({ source: "ainolez-preview", runId: ${JSON.stringify(runId)}, type: type, text: text }, "*"); }
  function show(value) {
    if (value instanceof Error) return value.message;
    if (typeof value === "object") { try { return JSON.stringify(value); } catch (e) { return String(value); } }
    return String(value);
  }
  send("ready", ""); // tells the editor the preview really loaded (see CodePageEditor)
  ["log", "info", "warn", "error"].forEach(function (level) {
    var original = console[level];
    console[level] = function () {
      send(level, Array.prototype.map.call(arguments, show).join(" "));
      original.apply(console, arguments);
    };
  });
  addEventListener("error", function (event) { send("error", event.message + (event.lineno ? " (line " + event.lineno + ")" : "")); });
  addEventListener("unhandledrejection", function (event) { send("error", "Unhandled promise: " + show(event.reason)); });
  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest("a[href]");
    if (!link || link.target) return;
    var href = link.getAttribute("href");
    if (!href || href.charAt(0) === "#") return;
    event.preventDefault();
    send("link", href);
  });
})();
</script>`;
}

export function isWholeDocument(html) {
  return WHOLE.test(html ?? "");
}

/** The page as the site shows it: a whole document as written, or a fragment wrapped in one. */
export function pageDocument({ title = "", html = "", css = "", js = "", runId = "" }) {
  const head = relay(runId) + (css.trim() ? style(css) : "");
  const tail = js.trim() ? script(js) : "";
  if (isWholeDocument(html)) {
    let page = insertBefore(html, /<\/head\s*>/gi, head) ?? insertAfterOpening(html, head);
    page = insertBefore(page, /<\/body\s*>/gi, tail) ?? page + tail;
    return page;
  }
  const safeTitle = title.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  return (
    `<!doctype html><html lang="en"><head><meta charset="utf-8">` +
    `<meta name="viewport" content="width=device-width, initial-scale=1">` +
    `<title>${safeTitle}</title><style>${BASE_CSS}</style>${head}</head><body>${html}${tail}</body></html>`
  );
}

function insertBefore(html, pattern, text) {
  const matches = [...html.matchAll(pattern)];
  if (!matches.length) return null;
  const at = matches[matches.length - 1].index;
  return html.slice(0, at) + text + html.slice(at);
}

function insertAfterOpening(html, text) {
  const match = html.match(/<html[^>]*>/i) ?? html.match(/<!doctype[^>]*>/i);
  if (!match) return text + html;
  const at = match.index + match[0].length;
  return html.slice(0, at) + text + html.slice(at);
}

/** Which tab a file goes to, by its extension. */
export function tabForFile(name) {
  const extension = name.toLowerCase().split(".").pop();
  if (extension === "html" || extension === "htm") return "code_html";
  if (extension === "css") return "code_css";
  if (extension === "js" || extension === "mjs") return "code_js";
  return null;
}

export const TEMPLATES = {
  landing: {
    label: "Landing section",
    code_html: `<section class="hero">
  <p class="eyebrow">ainolez</p>
  <h1>Learn it. Code it. <span>Own it.</span></h1>
  <p class="lead">Free, hands-on lessons in coding and AI.</p>
  <a class="button" href="/courses">Browse courses</a>
</section>

<section class="cards">
  <article><h3>Try it live</h3><p>Edit code and see the result at once.</p></article>
  <article><h3>Earn badges</h3><p>Points, streaks and certificates.</p></article>
  <article><h3>Ask the AI tutor</h3><p>Stuck? Get a hint, not the answer.</p></article>
</section>`,
    code_css: `.hero {
  padding: 72px 24px;
  text-align: center;
  color: #fff;
  background: radial-gradient(circle at 20% 0%, #0b3b5c, #05192d 60%);
}
.eyebrow { margin: 0; color: #03ef62; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; }
.hero h1 { margin: 12px 0; font-size: clamp(32px, 6vw, 56px); }
.hero h1 span { color: #03ef62; }
.lead { margin: 0 auto 28px; max-width: 520px; color: #c9d4e0; font-size: 18px; }
.button {
  display: inline-block; padding: 14px 26px; border-radius: 999px;
  background: #03ef62; color: #05192d; font-weight: 700; text-decoration: none;
}
.cards {
  display: grid; gap: 16px; padding: 48px 24px; max-width: 1040px; margin: 0 auto;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}
.cards article { padding: 24px; border: 1px solid #e3e8ef; border-radius: 14px; }
.cards h3 { margin-top: 0; }`,
    code_js: `// Fade the cards in as they scroll into view.
const cards = document.querySelectorAll(".cards article");
const watcher = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) entry.target.animate(
      [{ opacity: 0, transform: "translateY(16px)" }, { opacity: 1, transform: "none" }],
      { duration: 500, easing: "ease-out", fill: "both" },
    );
  }
});
cards.forEach((card) => watcher.observe(card));`,
  },
  game: {
    label: "Click game (JS)",
    code_html: `<main class="game">
  <h1>Catch the dot</h1>
  <p>Score: <strong id="score">0</strong> · Time: <strong id="time">20</strong>s</p>
  <div id="board"><button id="dot" aria-label="Dot"></button></div>
  <button id="start">Start</button>
</main>`,
    code_css: `.game { max-width: 640px; margin: 0 auto; padding: 32px 16px; text-align: center; }
#board { position: relative; height: 320px; margin: 16px 0; border-radius: 16px; background: #f5f7fa; overflow: hidden; }
#dot { position: absolute; width: 36px; height: 36px; border: 0; border-radius: 50%; background: #04aa6d; cursor: pointer; display: none; }
#start { padding: 12px 24px; border: 0; border-radius: 999px; background: #05192d; color: #fff; font-weight: 600; cursor: pointer; }`,
    code_js: `const board = document.getElementById("board");
const dot = document.getElementById("dot");
let score = 0, left = 0, timer;

function moveDot() {
  dot.style.left = Math.random() * (board.clientWidth - 36) + "px";
  dot.style.top = Math.random() * (board.clientHeight - 36) + "px";
}
dot.onclick = () => { score++; document.getElementById("score").textContent = score; moveDot(); };
document.getElementById("start").onclick = () => {
  score = 0; left = 20; dot.style.display = "block"; moveDot();
  clearInterval(timer);
  timer = setInterval(() => {
    document.getElementById("time").textContent = --left;
    if (left === 0) { clearInterval(timer); dot.style.display = "none"; alert("Score: " + score); }
  }, 1000);
};`,
  },
  blank: { label: "Empty page", code_html: "", code_css: "", code_js: "" },
};
