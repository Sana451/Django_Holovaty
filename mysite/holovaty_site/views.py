from django.http import HttpResponse, Http404
import datetime
from django.shortcuts import render


def my_homepage_view(request):
    return HttpResponse("HomePage")


def hello(request):
    return HttpResponse("Hello World")


def current_datetime(request):
    current_date = datetime.datetime.now()
    # print(locals())
    return render(request, "templ.html", locals())


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    assert False
    html = """
                <html>
                <body>
                Через {} ч.  будет {}
                </body>
                </html>
                """.format(offset, dt)
    return HttpResponse(html)
