from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib.comments.feeds import LatestCommentFeed
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from easy_blog.sitemaps import StoriesSitemap

urlpatterns = patterns('',
    url(r'^blog/',            include('easy_blog.urls')),
    url(r"^comments/",        include("django_comments_xtd.urls")),
)

sitemaps = {
    'stories': StoriesSitemap,
}

urlpatterns += patterns("django.contrib.sitemaps.views",
    url(r'^sitemap\.xml$',                 'index',   {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
