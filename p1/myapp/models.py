from django.db import models


# Create your models here.


class Site(models.Model):
    site_id = models.AutoField(db_column="id", primary_key=True)
    site_host = models.TextField(db_column="host")
    site_name = models.TextField(db_column="name")

    class Meta:
        db_table = "site"
        verbose_name = "Site"
        verbose_name_plural = "Sites"


class Page(models.Model):
    page_id = models.AutoField(primary_key=True, db_column="id")
    page_site_id = models.ForeignKey('Site', on_delete=models.CASCADE, db_column="site_id")
    page_url = models.TextField(db_column="url")

    class Meta:
        db_table = "page"
        verbose_name = "Page"
        verbose_name_plural = "Pages"


class Content(models.Model):
    content_id = models.AutoField(primary_key=True, db_column="id")
    content_page_id = models.ForeignKey('Page', on_delete=models.CASCADE, db_column="page_id")
    content_basic = models.TextField(db_column="basic information")
    content_ignored = models.TextField(db_column="ignored information")
    content_deleted = models.TextField(db_column="deleted information")

    class Meta:
        db_table = "content"
        verbose_name = "Content"
        verbose_name_plural = "Contents"


class Request(models.Model):
    request_id = models.AutoField(primary_key=True, db_column="id")
    request_content_id = models.ForeignKey('Content', on_delete=models.CASCADE, db_column="content_id")
    request_datetime = models.DateTimeField(auto_now=True, db_column="datetime")

    class Meta:
        db_table = "request"
        verbose_name = "Request"
        verbose_name_plural = "Requests"
