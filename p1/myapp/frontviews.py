from .models import Request

from django.template.response import TemplateResponse


def main(request):
    return TemplateResponse(request, "Main.html")


def req(request):
    return TemplateResponse(request, "Request.html")


def history(request):
    requests = Request.objects.all()
    data = []
    for i in requests:
        n = []
        n.append(i.request_id)
        n.append(i.request_content_id.content_page_id.page_url)
        n.append(i.request_content_id.content_page_id.page_site_id.site_name)
        n.append(i.request_datetime)
        data.append(n)
    return TemplateResponse(request, "History.html", context={"data": data})
