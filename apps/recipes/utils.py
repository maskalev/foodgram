import io

from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from foodgram.settings import STATIC_ROOT

TYPEFACE = 'Arial'
TYPEFACE_FILE = 'fonts/arial.ttf'
HEAD_FONTSIZE = 40
HEAD_X = 150
HEAD_Y = 800
HEAD_TEXT = 'Список покупок'
BODY_FONTSIZE = 20
BODY_X = 50
BODY_Y = 750
BODY_LINE_SPACING = 50


def create_pdf(ingredients, filename):
    """
    Create purchase list.
    """
    def print_head():
        pdf_canvas.setFont(TYPEFACE, HEAD_FONTSIZE)
        pdf_canvas.drawString(HEAD_X, HEAD_Y, HEAD_TEXT)
        pdf_canvas.setFont(TYPEFACE, BODY_FONTSIZE)

    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer)
    font = ttfonts.TTFont(TYPEFACE, STATIC_ROOT / TYPEFACE_FILE)
    pdfmetrics.registerFont(font)
    print_head()
    line_y = -1
    for pos, val in enumerate(ingredients, start=1):
        line_y += 1
        string = (f'{pos}. {val["recipe__ingredients__title"]} '
                  f'({val["recipe__ingredients__unit"]}): '
                  f'{val["quantity"]}')
        pdf_canvas.drawString(BODY_X,
                              BODY_Y - BODY_LINE_SPACING * line_y,
                              string)
        if (pos + 1) % 15 == 0:
            pdf_canvas.showPage()
            line_y = -1
            print_head()

    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)
