from django.http import Http404, HttpResponse
from django.utils.html import escape
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.catalog import selectors as catalog
from modules.certification import selectors, services

DESCRIPTION = "A verified certificate from ainolez, free coding and AI courses."


class CertificateView(APIView):
    """Public verify page data: anyone with the code can check a certificate."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, code):
        cert = selectors.public_certificate(code)
        if cert is None:
            raise Http404
        services.count_view(cert)
        share_url = request.build_absolute_uri(f"/share/certificates/{cert.certificate_code}/")
        course = catalog.course_summaries([cert.course_id]).get(cert.course_id, {})
        return Response({
            "code": cert.certificate_code,
            "status": cert.status,
            "learner_name": cert.learner_name,
            "course_title": cert.course_title,
            "course_slug": course.get("slug"),
            "issued_at": cert.issued_at,
            "revoked_at": cert.revoked_at,
            "revoke_reason": cert.revoke_reason,
            "verify_url": cert.verify_url,
            "share_url": share_url,
            "pdf_url": cert.pdf_url,
            "image_url": cert.image_url,
        })  # fmt: skip


def share_page(request, code):
    """
    The link people post on LinkedIn, X or Facebook. Their crawlers read the Open
    Graph tags here (the React app cannot provide them); people are sent on to
    the certificate page.
    """
    cert = selectors.public_certificate(code)
    if cert is None:
        raise Http404
    title = escape(f"{cert.learner_name} completed {cert.course_title}")
    image = escape(request.build_absolute_uri(cert.image_url)) if cert.image_url else ""
    url = escape(cert.verify_url)
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title} · ainolez</title>
<meta property="og:type" content="website">
<meta property="og:site_name" content="ainolez">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{url}">
{f'<meta property="og:image" content="{image}">' if image else ""}
<meta name="twitter:card" content="summary_large_image">
<meta http-equiv="refresh" content="0; url={url}">
</head><body><a href="{url}">View the certificate</a></body></html>"""
    return HttpResponse(html)
