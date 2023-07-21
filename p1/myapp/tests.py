from unittest import TestCase

from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import Client, RequestFactory
from http import HTTPStatus
from .models import Request
from .views import Main


class UserTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_is_ok_main(self):
        response = self.c.get('http://127.0.0.1:8000/myapp/main/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_is_ok_request(self):
        response = self.c.get('http://127.0.0.1:8000/myapp/main/request/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_is_ok_history(self):
        response = self.c.get('http://127.0.0.1:8000/myapp/main/history/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_button(self):
        request_factory = RequestFactory()
        data = {'fname': 'https://tomsk-gorod.ru/kak-dolgo-zhivut-babochki-ili-skolko-vremeni-dlitsya-ih-zhizn/',
                'lname': 'томск город ру'}
        request = request_factory.post('http://127.0.0.1:8000/myapp/main/request/', data=data)
        response = Main.as_view()(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_database(self):
        requests = Request.objects.all()
        data = []
        for i in requests:
            response = self.c.get('http://127.0.0.1:8000/myapp/main/request/work/' + str(i.request_id) + '/')
            header_number = i.request_id
            requests = Request.objects.get(request_id=i.request_id)
            text = requests.request_content_id.content_basic
            header_url = requests.request_content_id.content_page_id.page_url
            header_site = requests.request_content_id.content_page_id.page_site_id.site_name
            header_host = requests.request_content_id.content_page_id.page_site_id.site_host

            self.assertEqual(response.context["header_number"], header_number,
                             'В основной информации запросе №' + str(i.request_id) + ' не совпадение номера запроса')
            self.assertEqual(response.context["header_site"], header_site, 'В основной информации запросе №' + str(
                i.request_id) + ' не совпадение названия сайта запроса')
            self.assertEqual(response.context["header_url"], header_url,
                             'В основной информации запросе №' + str(i.request_id) + ' не совпадение url запроса')
            self.assertEqual(response.context["header_host"], header_host,
                             'В основной информации запросе №' + str(i.request_id) + ' не совпадение хоста запроса')
            self.assertEqual(response.context["text"], text,
                             'В основной информации запросе №' + str(i.request_id) + ' не совпадение текста запроса')

            response = self.c.get('http://127.0.0.1:8000/myapp/main/request/work/' + str(i.request_id) + '/deleted/')
            header_number = i.request_id
            requests = Request.objects.get(request_id=i.request_id)
            text = requests.request_content_id.content_deleted
            header_url = requests.request_content_id.content_page_id.page_url
            header_site = requests.request_content_id.content_page_id.page_site_id.site_name
            header_host = requests.request_content_id.content_page_id.page_site_id.site_host

            self.assertEqual(response.context["header_number"], header_number,
                             'В удаляемой информации запросе №' + str(i.request_id) + ' не совпадение номера запроса')
            self.assertEqual(response.context["header_site"], header_site, 'В удаляемой информации запросе №' + str(
                i.request_id) + ' не совпадение названия сайта запроса')
            self.assertEqual(response.context["header_url"], header_url,
                             'В удаляемой информации запросе №' + str(i.request_id) + ' не совпадение url запроса')
            self.assertEqual(response.context["header_host"], header_host,
                             'В удаляемой информации запросе №' + str(i.request_id) + ' не совпадение хоста запроса')
            self.assertEqual(response.context["text"], text,
                             'В удаляемой информации запросе №' + str(i.request_id) + ' не совпадение текста запроса')

            response = self.c.get('http://127.0.0.1:8000/myapp/main/request/work/' + str(i.request_id) + '/ignored/')
            header_number = i.request_id
            requests = Request.objects.get(request_id=i.request_id)
            text = requests.request_content_id.content_ignored
            header_url = requests.request_content_id.content_page_id.page_url
            header_site = requests.request_content_id.content_page_id.page_site_id.site_name
            header_host = requests.request_content_id.content_page_id.page_site_id.site_host

            self.assertEqual(response.context["header_number"], header_number,
                             'В игнорируемой информации запросе №' + str(
                                 i.request_id) + ' не совпадение номера запроса')
            self.assertEqual(response.context["header_site"], header_site, 'В игнорируемой информации запросе №' + str(
                i.request_id) + ' не совпадение названия сайта запроса')
            self.assertEqual(response.context["header_url"], header_url,
                             'В игнорируемой информации запросе №' + str(i.request_id) + ' не совпадение url запроса')
            self.assertEqual(response.context["header_host"], header_host,
                             'В игнорируемой информации запросе №' + str(i.request_id) + ' не совпадение хоста запроса')
            self.assertEqual(response.context["text"], text,
                             'В игнорируемой информации запросе №' + str(
                                 i.request_id) + ' не совпадение текста запроса')

            n = []
            n.append(i.request_id)
            n.append(i.request_content_id.content_page_id.page_url)
            n.append(i.request_content_id.content_page_id.page_site_id.site_name)
            n.append(i.request_datetime)
            data.append(n)
        response = self.c.get('http://127.0.0.1:8000/myapp/main/history/')
        self.assertEqual(response.context["data"], data)
