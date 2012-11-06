from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic

from easy_blog.models import Story
from easy_blog.views import (StoryDetailView, StoryListView, StoryYearArchiveView,
                             StoryMonthArchiveView, StoryDayArchiveView)


page_size       = getattr(settings, "EASY_BLOG_PAGINATE_BY", 10)
large_page_size = getattr(settings, "EASY_BLOG_PAGINATE_BY", 10) * 2

urlpatterns = patterns('',

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        StoryDetailView.as_view(
            queryset=Story.objects.published(),
            date_field="pub_date", month_format="%m", 
            template_name="easy_blog/story_detail.html"),
        name='blog-story-detail-month-numeric'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        StoryDetailView.as_view(
            queryset=Story.objects.published(),            
            date_field="pub_date", month_format="%b", 
            template_name="easy_blog/story_detail.html"),
        name='blog-story-detail'),

    # allowing access to a story in draft mode
    url(r'^draft/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        login_required(
            permission_required('easy_blog.can_see_unpublished_stories')(
                generic.DateDetailView.as_view(
                    queryset=Story.objects.drafts(),
                    date_field="pub_date", month_format="%b", 
                    template_name="easy_blog/story_detail.html", allow_future=True)
                ),
            redirect_field_name=""),
        name='blog-story-detail-draft'),

    # allowing access to a story in review mode
    url(r'^review/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        login_required(
            permission_required('easy_blog.can_review_stories')(
                generic.DateDetailView.as_view(
                    model=Story, date_field="pub_date", month_format="%b", 
                    template_name="easy_blog/story_detail.html", allow_future=True)
                ),
            redirect_field_name=""),
        name='blog-story-detail-review'),

    # allowing access to an upcoming storie
    url(r'^upcoming/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        login_required(
            permission_required('easy_blog.can_see_unpublished_stories')(
                generic.DateDetailView.as_view(
                    queryset=Story.objects.upcoming(),
                    date_field="pub_date", month_format="%b", 
                    template_name="easy_blog/story_detail.html", allow_future=True)
                ),
                redirect_field_name=""),
        name='blog-story-detail-upcoming'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        StoryDayArchiveView.as_view(model=Story, paginate_by=page_size),
        name='blog-story-archive-day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        StoryMonthArchiveView.as_view(model=Story, paginate_by=page_size),
        name='blog-story-archive-month'),

    url(r'^(?P<year>\d{4})/$',
        StoryYearArchiveView.as_view(model=Story, paginate_by=large_page_size),
        name='blog-story-archive-year'),

    url(r'^$', StoryListView.as_view(
            model=Story, paginate_by=page_size,
            template_name="easy_blog/story_list.html"), 
        name='blog-story-list'),
)
