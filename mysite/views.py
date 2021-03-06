# encoding:utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from mysite.books.models import Book, Publisher, Author

import datetime
import csv
import logging
# from django.views.generic import list_detail
from reportlab.pdfgen import canvas
from cStringIO import StringIO
from django.core.context_processors import csrf
from CommonBus.jingdong import JD
from CommonBus.WeChat import WeChat
from django.utils.encoding import smart_str, smart_unicode

UNRULY_PASSENGERS = [146, 184, 235, 200, 226, 251, 299, 273, 281, 304, 203]
class StaticVariable(object):
    count = 0
def hello(request):
    return HttpResponse("Hello World")

def welcome(request):
    StaticVariable.count += 1
    print StaticVariable.count
    return HttpResponse("Welcome|%s" % StaticVariable.count)

def error(request):
    return HttpResponse("找不到该页面")

def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html><body>This is now %s</body></html>' % (now)
    return HttpResponse(html)

def search(request):
    return render_to_response('search.html', {'aa':'bb'})

def books_by_publisher(request, name):
    pass
#     # 查询publisher(如果不存在则抛出404错误).
#     publisher = get_object_or_404(Publisher, name = name)
#     #Use the object_list view for the heavy lifting.
#     return list_detail.object_list(request,
#                                     queryset = Book.objects.filter(publisher = publisher),
#                                     template_name = 'books_by_object.html',
#                                     extra_context = {'publisher':publisher},
#                                     template_object_name = 'book')

def author_detail(request, author_id):
    pass
#     response = list_detail.object_detail(request, queryset = Author.objects.all(),
#                                          object_id = author_id,
#                                          template_name = 'author_detail.html',
#                                          template_object_name = 'author')
#     now = datetime.datetime.now()
#     Author.objects.filter(id = author_id).update(last_accessed = now)
#     return response

def author_list_plaintext(request):
    pass
#     response = list_detail.object_list(request,
#                                        queryset = Author.objects.all(),
#                                        template_name = 'author_list_plaintext.html',
#                                        mimetype = 'text/plain',
#                                        template_object_name = 'author')
#     response['Content-Disposition'] = 'attachment;filename=authors.txt'
#     return response

def my_image(request):
    image_data = open('e:/eclipse/mysite/mysite/background.png', 'rb').read()
    return HttpResponse(image_data, mimetype='image/png')

def unruly_passengers_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/html')
    response['Content-Disposition'] = 'attachment;filename=unruly.csv'
    # Create the CSV writer using the HttpResponse as the "file."
    writer = csv.writer(response)
    writer.writerow(['Year,Unruly Airline Passengers'])
    for (year, num) in zip(range(1995, 2006), UNRULY_PASSENGERS):
        writer.writerow([year, num])
    return response

def hello_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Dispositon'] = 'attachment;filename=hello.pdf'
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # 从某个文件中读取数据写到PDF中(含中文的不会)
#    open('C:\Users\ke\Desktop\新建文本文档.txt').read()
#    s = unicode(open('C:/Users/ke/Desktop/22.txt', 'rb').read(), 'GBK')
    s = 'Hello World'
    p.drawString(100, 100, s)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

# 效率更高
def hello_cStringIO(request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Dispositon'] = 'attachment;filename=hello.pdf'
    temp = StringIO()
    p = canvas.Canvas(temp)
    # 不能用汉字
    s = 'Hello World'
    p.drawString(100, 100, s)
    p.showPage()
    p.save()
    response.write(temp.getvalue())
    return response

def login(request):
#    image_data = open('e:/eclipse/mysite/mysite/background.png', 'rb').read()
    r = {}
    r.update(csrf(request))
    return render_to_response('login.html', r)

def index(request):
    return render_to_response('index.html', {'account':request.post('account'), 'password':request.post('password')})

def modifyBookName(request, id, title):
    book = Book.objects.filter(id=id).update(title=title)
    return welcome(request)

def test_cookie(request):
    msg = None
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
#        check that the test cookie worked(we set it below)
        msg = 'cookie is exist'
    else:
        msg = 'cookie is not exist'
    request.session.set_test_cookie()
    request.session['name'] = 'ke'
    return HttpResponse(request.session['name'])

def showascii(request):
    return render_to_response('ascii.html')

def wx(request):
    print '/wx Enter'
    wx = WeChat()
    if request.method == 'POST':
        print 'post'
        return HttpResponse(wx.getMsg(request), content_type="application/xml")
    elif request.method == 'GET':
        print 'get'
        return HttpResponse(wx.checkSign(request))


def ltc(request):
    ltc = open('/home/hhhyde/ServerMapping/LTCPriceRecord').readlines()
    ltc.reverse()
    return HttpResponse(r'<hr>'.join(ltc))
    
def reminder(request, reminder):
    try:
        reminder = float(reminder)
        reminderFile = open('/root/CronScript/LTCPriceRemind', 'w')
        reminderFile.write(str(reminder))
        reminderFile.close()
        return HttpResponse('OK')
    except Exception, e:
        logging.info(r'views\treminder\taccept an unnumeric type')

def jqgrid(request):
    LTCPriceRecord = open('/home/hhhyde/ServerMapping/LTCPriceRecord').readlines()
    LTCPriceRecord.reverse()
    result = []
    for record in LTCPriceRecord:
        price = record.split()[0]
        time = record.split()[2]
        result.append({'id':price, 'invdate':time})
    a = [{'price':1, 'time':'2007-10-11'}, {'price':12, 'time':'2007-10-12'}]
    return render_to_response('myfirstgrid.html', {'LTCRecord':result})

def dw(request):
    return render_to_response('dw.html')
