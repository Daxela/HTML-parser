# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse

from .models import Site
from .serializers import SiteSerializer
from .models import Page
from .serializers import PageSerializer
from .models import Request
from .serializers import RequestSerializer
from .models import Content
from .serializers import ContentSerializer
from rest_framework.views import APIView
from .WebProcessor.processor import processing
from django.template.response import TemplateResponse


class Main(APIView):

    def post(self, request):
        url = request.POST.get("fname")
        name_site = request.POST.get("lname")

        header_site = name_site
        header_url = url

        k = 0
        num = 0
        num_n = 0
        flag = True
        for char in url:
            num = num + 1
            if char == '/':
                k = k + 1
            if (k == 2) & flag:
                num_n = num
                flag = False
            if k == 3:
                host = url[num_n:num - 1]
                break

        header_host = host

        if not Site.objects.filter(site_name=name_site, site_host=host).exists():
            datakey = ["site_id", "site_host", "site_name"]
            data = dict.fromkeys(datakey)

            data['site_host'] = host
            data['site_name'] = name_site
            site_serializer = SiteSerializer(data=data)
            if site_serializer.is_valid():
                site_serializer.save()

        site = Site.objects.get(site_name=name_site, site_host=host)
        site_id = site.site_id

        if not Page.objects.filter(page_url=url, page_site_id=site_id).exists():
            datakey = ["page_id", "page_site_id", "page_url"]
            data = dict.fromkeys(datakey)

            data['page_site_id'] = site_id
            data['page_url'] = url
            page_serializer = PageSerializer(data=data)
            if page_serializer.is_valid():
                page_serializer.save()

        page = Page.objects.get(page_site_id=site_id, page_url=url)
        page_id = page.page_id

        if not Content.objects.filter(content_page_id=page_id).exists():
            datakey = ["content_id", "content_page_id", "content_class", "content_content"]
            data = dict.fromkeys(datakey)

            data['content_page_id'] = page_id

            basic, ignored, deleted = processing(url)

            data['content_ignored'] = ignored
            data['content_basic'] = basic
            data['content_deleted'] = deleted
            content_serializer = ContentSerializer(data=data)
            if content_serializer.is_valid():
                content_serializer.save()

        content = Content.objects.get(content_page_id=page_id)
        content_id = content.content_id
        text = content.content_basic

        if not Request.objects.filter(request_content_id=content_id).exists():
            datakey = ["request_id", "request_content_id", "request_datetime"]
            data = dict.fromkeys(datakey)
            data['request_content_id'] = content_id
            request_serializer = RequestSerializer(data=data)
            if request_serializer.is_valid():
                request_serializer.save()

        request_t = Request.objects.get(request_content_id=content_id)
        request_id = request_t.request_id
        header_number = request_id

        key = ["header_number", "header_site", "header_url", "header_host", "text"]
        data = dict.fromkeys(key)
        data['header_number'] = header_number
        data['header_site'] = header_site
        data['header_url'] = header_url
        data['header_host'] = header_host
        data['text'] = text

        return TemplateResponse(request, "Result.html", data)


class Basic(APIView):

    def get(self, request, request_id):
        header_number = request_id
        requests = Request.objects.get(request_id=request_id)
        text = requests.request_content_id.content_basic
        header_url = requests.request_content_id.content_page_id.page_url
        header_site = requests.request_content_id.content_page_id.page_site_id.site_name
        header_host = requests.request_content_id.content_page_id.page_site_id.site_host

        key = ["header_number", "header_site", "header_url", "header_host", "text"]
        data = dict.fromkeys(key)
        data['header_number'] = header_number
        data['header_site'] = header_site
        data['header_url'] = header_url
        data['header_host'] = header_host
        data['text'] = text

        return TemplateResponse(request, "Result.html", data)


class Del(APIView):

    def get(self, request, request_id):
        header_number = request_id
        requests = Request.objects.get(request_id=request_id)
        text = requests.request_content_id.content_deleted
        header_url = requests.request_content_id.content_page_id.page_url
        header_site = requests.request_content_id.content_page_id.page_site_id.site_name
        header_host = requests.request_content_id.content_page_id.page_site_id.site_host

        key = ["header_number", "header_site", "header_url", "header_host", "text"]
        data = dict.fromkeys(key)
        data['header_number'] = header_number
        data['header_site'] = header_site
        data['header_url'] = header_url
        data['header_host'] = header_host
        data['text'] = text

        return TemplateResponse(request, "Deleted.html", data)


class Ign(APIView):

    def get(self, request, request_id):
        header_number = request_id
        requests = Request.objects.get(request_id=request_id)
        text = requests.request_content_id.content_ignored
        header_url = requests.request_content_id.content_page_id.page_url
        header_site = requests.request_content_id.content_page_id.page_site_id.site_name
        header_host = requests.request_content_id.content_page_id.page_site_id.site_host

        key = ["header_number", "header_site", "header_url", "header_host", "text"]
        data = dict.fromkeys(key)
        data['header_number'] = header_number
        data['header_site'] = header_site
        data['header_url'] = header_url
        data['header_host'] = header_host
        data['text'] = text

        return TemplateResponse(request, "Ignored.html", data)

def my_view(request):
    return redirect('myapp/main/')
