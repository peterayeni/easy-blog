#-*- coding: utf-8 -*-
import datetime
from django.contrib.sitemaps import Sitemap

from easy_blog.models import Story


class StoriesSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Story.objects.filter(
            status__gte=2, 
            pub_date__lte=datetime.datetime.now()).order_by("-pub_date")

    def lastmod(self, obj):
        return obj.mod_date
