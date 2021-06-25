import io

from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from foodgram.settings import (PDF_BODY_FONTSIZE, PDF_HEAD_FONTSIZE,
                               PDF_HEAD_TEXT, PDF_HEAD_X, PDF_HEAD_Y,
                               PDF_TYPEFACE, STATIC_ROOT)


def create_pdf(ingredients, filename):
    """
    Create purchase list.
    """
    def print_head():
        pdf_canvas.setFont(PDF_TYPEFACE, PDF_HEAD_FONTSIZE)
        pdf_canvas.drawString(PDF_HEAD_X, PDF_HEAD_Y, PDF_HEAD_TEXT)
        pdf_canvas.setFont(PDF_TYPEFACE, PDF_BODY_FONTSIZE)

    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer)
    font = ttfonts.TTFont(PDF_TYPEFACE, STATIC_ROOT / 'fonts/arial.ttf')
    pdfmetrics.registerFont(font)
    print_head()
    line_y = -1
    for pos, val in enumerate(ingredients):
        line_y += 1
        string = (f'{pos + 1}. {val["recipe__ingredients__title"]} '
                  f'({val["recipe__ingredients__unit"]}): '
                  f'{val["quantity"] or ""}')
        pdf_canvas.drawString(50, 750 - 50 * line_y, string)
        if (pos + 1) % 15 == 0:
            pdf_canvas.showPage()
            line_y = -1
            print_head()

    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)
