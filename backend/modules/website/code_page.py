"""
The document of a custom code page: the admin's HTML with their CSS and
JavaScript put in place, plus a small helper script that tells the website
how tall the page is and passes link clicks up to it.

The API serves it with a `sandbox` Content-Security-Policy, so even opened
directly its scripts get an opaque origin (no API cookies or storage), and the
website shows it in a sandboxed iframe. Keep `pageDocument` in
frontend/src/features/admin/website/codePage.js the same (the admin preview).
"""

import re

HELPER = """<script>
(function () {
  function send(data) { data.source = "ainolez-page"; parent.postMessage(data, "*"); }
  function height() {
    var d = document.documentElement, b = document.body;
    send({ type: "height", height: Math.max(d.scrollHeight, b ? b.scrollHeight : 0) });
  }
  addEventListener("load", function () { height(); send({ type: "ready" }); });
  addEventListener("resize", height);
  if (window.ResizeObserver) new ResizeObserver(height).observe(document.documentElement);
  // Links open on the website (the frame cannot leave itself); #anchors stay here.
  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest("a[href]");
    if (!link || event.defaultPrevented || link.target) return;
    var href = link.getAttribute("href");
    if (!href || href.charAt(0) === "#") return;
    event.preventDefault();
    send({ type: "navigate", href: href });
  });
})();
</script>"""

BASE_CSS = "html,body{margin:0}body{font-family:Inter,'Segoe UI',Arial,sans-serif}"
WHOLE = re.compile(r"^\s*(<!doctype|<html)", re.IGNORECASE)
HEAD_END = re.compile(r"</head\s*>", re.IGNORECASE)
BODY_END = re.compile(r"</body\s*>", re.IGNORECASE)


def _script(code: str) -> str:
    # "</script" inside the code would end the tag early.
    return "<script>" + re.sub(r"</(script)", r"<\\/\1", code, flags=re.IGNORECASE) + "</script>"


def _style(code: str) -> str:
    return "<style>" + re.sub(r"</(style)", r"<\\/\1", code, flags=re.IGNORECASE) + "</style>"


def document(title: str, html: str, css: str, js: str) -> str:
    """A whole HTML document is kept as written; a fragment gets a page around it."""
    head = HELPER + (_style(css) if css.strip() else "")
    tail = _script(js) if js.strip() else ""
    if WHOLE.match(html):
        html = _insert(HEAD_END, html, head, before=True) or _insert_after_html(html, head)
        return _insert(BODY_END, html, tail, before=True) or html + tail
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{_escape(title)}</title><style>{BASE_CSS}</style>{head}</head>"
        f"<body>{html}{tail}</body></html>"
    )


def _insert(pattern: re.Pattern, html: str, text: str, before: bool) -> str | None:
    matches = list(pattern.finditer(html))
    if not matches:
        return None
    at = matches[-1].start() if before else matches[-1].end()
    return html[:at] + text + html[at:]


def _insert_after_html(html: str, text: str) -> str:
    match = re.search(r"<html[^>]*>", html, re.IGNORECASE)
    if match:
        return html[: match.end()] + text + html[match.end() :]
    match = re.search(r"<!doctype[^>]*>", html, re.IGNORECASE)
    return html[: match.end()] + text + html[match.end() :] if match else text + html


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
