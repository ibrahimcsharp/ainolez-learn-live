"""Draws a certificate as an A4 PDF (reportlab) and a 1200x627 share image (Pillow)."""

import io

from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from modules.certification.models import Certificate, CertificateTemplate

INK = "#1F2933"
GREY = "#67748A"


def certificate_pdf(cert: Certificate, template: CertificateTemplate) -> bytes:
    buffer = io.BytesIO()
    width, height = landscape(A4)
    pdf = canvas.Canvas(buffer, pagesize=(width, height))
    pdf.setTitle(f"{cert.course_title} - {cert.learner_name}")
    primary, accent = HexColor(template.primary_color), HexColor(template.accent_color)

    # Frame: navy band on the left with the wordmark, thin accent line.
    pdf.setFillColor(primary)
    pdf.rect(0, 0, 150, height, stroke=0, fill=1)
    pdf.setFillColor(accent)
    pdf.rect(150, 0, 6, height, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(75, height - 80, "ainolez")
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(75, height - 98, "Learn it. Code it. Own it.")

    center = 156 + (width - 156) / 2
    lines = [
        ("Helvetica-Bold", 30, primary, height - 130, template.heading),
        ("Helvetica", 14, HexColor(GREY), height - 185, "This certifies that"),
        ("Helvetica-Bold", 36, HexColor(INK), height - 240, cert.learner_name),
        ("Helvetica", 14, HexColor(GREY), height - 285, template.body_text),
        ("Helvetica-Bold", 22, primary, height - 325, cert.course_title),
    ]
    for font, size, color, y, text in lines:
        pdf.setFont(font, size)
        pdf.setFillColor(color)
        pdf.drawCentredString(center, y, text)

    # Footer: date and signer on the left, code and QR on the right.
    pdf.setFillColor(HexColor(INK))
    pdf.setFont("Helvetica", 11)
    pdf.drawString(200, 110, f"Issued {cert.issued_at:%d %B %Y}")
    pdf.drawString(200, 92, template.signer_name)
    pdf.setFillColor(HexColor(GREY))
    pdf.drawString(200, 76, template.signer_title)
    pdf.drawRightString(width - 150, 110, f"Certificate ID {cert.certificate_code}")
    pdf.setFont("Helvetica", 9)
    pdf.drawRightString(width - 150, 94, cert.verify_url)

    qr = QrCodeWidget(cert.verify_url)
    x0, y0, x1, y1 = qr.getBounds()
    drawing = Drawing(90, 90, transform=[90 / (x1 - x0), 0, 0, 90 / (y1 - y0), 0, 0])
    drawing.add(qr)
    renderPDF.draw(drawing, pdf, width - 135, 60)

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def share_image(cert: Certificate, template: CertificateTemplate) -> bytes:
    """The picture LinkedIn, X and Facebook show when the certificate link is shared."""
    image = Image.new("RGB", (1200, 627), template.primary_color)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 607, 1200, 627), fill=template.accent_color)

    def text(xy, value, size, fill="#FFFFFF"):
        draw.text(xy, value, font=ImageFont.load_default(size=size), fill=fill)

    _wordmark(draw, (80, 70), 54, template.accent_color, template.primary_color)
    text((80, 190), template.heading.upper(), 30, template.accent_color)
    text((80, 250), _fit(cert.learner_name, 32), 72)
    text((80, 360), _fit(cert.course_title, 44), 44, "#C8D3E0")
    text((80, 520), f"Verified certificate  ·  ID {cert.certificate_code}", 26, "#C8D3E0")

    buffer = io.BytesIO()
    image.save(buffer, "PNG", optimize=True)
    return buffer.getvalue()


def _wordmark(draw, xy: tuple[int, int], size: int, cursor: str, background: str) -> None:
    """'ainolez' whose i-dot is the brand's square cursor (the font's dot is painted over)."""
    font = ImageFont.load_default(size=size)
    x, y = xy
    draw.text((x, y), "ainolez", font=font, fill="#FFFFFF")
    i_x = x + draw.textlength("a", font=font)
    i_box = draw.textbbox((i_x, y), "i", font=font)
    stem_top = draw.textbbox((i_x, y), "n", font=font)[1]
    draw.rectangle((i_box[0] - 2, i_box[1] - 2, i_box[2] + 2, stem_top - 3), fill=background)
    side = size * 0.24
    center = (i_box[0] + i_box[2]) / 2
    draw.rectangle(
        (center - side / 2, stem_top - side * 1.5, center + side / 2, stem_top - side * 0.5),
        fill=cursor,
    )


def _fit(value: str, max_chars: int) -> str:
    return value if len(value) <= max_chars else value[: max_chars - 1] + "…"
