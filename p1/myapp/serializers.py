from rest_framework import serializers
from .models import Site
from .models import Page
from .models import Request
from .models import Content

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class PagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['page_url', 'page_site_id']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class PageExpandSerializer(serializers.ModelSerializer):
    page_site_id = SiteSerializer(read_only=True)

    class Meta:
        model = Page
        fields = '__all__'


