"""
The Try-it sandbox page. Learners' HTML, CSS and JavaScript run in an iframe of
this page, which lives on the API's domain: a different origin from the website,
so the website can keep a strict Content-Security-Policy and learner code can
never reach its pages, cookies or storage (the iframe is also sandboxed).

The website posts the document to run; the page writes it into itself.
"""

from django.conf import settings
from django.http import HttpResponse

PAGE = """<!doctype html><meta charset="utf-8"><title>Result</title>
<script>
addEventListener("message", function (event) {
  if (event.source !== parent || !event.data || event.data.source !== "ainolez-run") return;
  document.open();
  document.write(event.data.html);
  document.close();
}, { once: true });
</script>"""


def runner(request):
    response = HttpResponse(PAGE)
    response["Content-Security-Policy"] = f"frame-ancestors 'self' {settings.FRONTEND_URL}"
    response["Cache-Control"] = "public, max-age=86400"
    return response
