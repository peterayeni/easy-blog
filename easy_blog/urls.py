#-*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.contrib.comments.feeds import LatestCommentFeed
from django.views.generic import DetailView, ListView, TemplateView

from tagging.models import Tag
from django_comments_xtd.models import XtdComment

from easy_blog import views
from easy_blog.feeds import LatestStoriesFeed, PostsByTag
from easy_blog.sitemaps import StoriesSitemap


page_size = getattr(settings, "EASY_BLOG_PAGINATE_BY", 10)
ui_columns = getattr(settings, "EASY_BLOG_UI_COLUMNS", 3)
search_url_active = getattr(settings, "EASY_BLOG_SEARCH_URL_ACTIVE", True)

urlpatterns = patterns("",
    url(r"^$", views.HomepageView.as_view(), name="blog-index"),
    url(r"^stories/", include("easy_blog.story_urls")),
 
    url(r"^tags$",
        TemplateView.as_view(template_name="easy_blog/tag_list.html"),
        name="blog-tag-list"),

    url(r"^tags/(?P<slug>.{1,50})$",
        views.TagDetailView.as_view(),
        name="blog-tag-detail"),

    url(r"^comments$", 
        ListView.as_view(
            queryset=XtdComment.objects.for_app_models("easy_blog.story"), 
            template_name="easy_blog/comment_list.html",
            paginate_by=page_size),
        name="blog-comment-list"),

    url(r'^feeds/stories/$', LatestStoriesFeed(), name='latest-stories-feed'),
    url(r'^feeds/comments/$', LatestCommentFeed(), name='comments-feed'),
    url(r"^feeds/tag/(?P<slug>.{1,50})$", PostsByTag(), name='posts-tagged-as'),

    url(r"^unpublished-on/$", views.show_unpublished, name="blog-unpublished-on"),
    url(r"^unpublished-off/$", views.hide_unpublished, name="blog-unpublished-off"),

    url(r'^inline-media/', include('inline_media.urls')),
)

#-- sitemaps ------------------------------------------------------------------
# if django-easy-blog is hooked at '/', activate the following code, otherwise
# add the StoriesSitemap class to your '/' URLConf
# sitemaps = {
#     'stories': StoriesSitemap,
# }

# urlpatterns += patterns("django.contrib.sitemaps.views",
#     url(r'^sitemap\.xml$',                 'index',   {'sitemaps': sitemaps}),
#     url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
# )
#------------------------------------------------------------------------------

#-- search --------------------------------------------------------------------
# set EASY_BLOG_SEARCH_URL_ACTIVE=False to avoid this hook

if search_url_active:
    from haystack.forms import SearchForm
    from haystack.views import SearchView, search_view_factory

    urlpatterns += patterns("",
        url(r'^search$', 
            search_view_factory(view_class=SearchView, 
                                form_class=SearchForm,
                                results_per_page=page_size), 
            name='haystack-search'),
    )
#------------------------------------------------------------------------------

