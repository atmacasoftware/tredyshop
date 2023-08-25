from io import BytesIO

from django.http import HttpResponse
import xlwt
from datetime import timedelta, datetime, date

from django.template.loader import get_template
from xhtml2pdf import pisa

from adminpage.models import Notification
from ecommerce import settings


def exportExcel(filename, sheetname, columns, rows):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = f'attachment; filename={filename}-' + str(datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'{sheetname}')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = columns
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = rows
    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response

def exportPdf(template_name, context_dict={}):
    template = get_template(template_name)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def notReadNotification():
    notify = Notification.objects.filter(is_read=False).count()
    return notify

def readNotification():
    notify = Notification.objects.filter(is_read=False)
    return notify

def createNotification(type, title, detail):
    notify = Notification.objects.create(noti_type=type, title=title, detail=detail)
    notify.save()
    response = 'Create Notify'
    return response