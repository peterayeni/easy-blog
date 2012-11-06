#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F, Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response as render
from django.template import RequestContext
try:
    from django.utils.timezone import now
except ImportError:
    from easy_blog.utils import now
from django.utils.translation import ugettext as _
from django.views.generic import View, ListView, DateDetailView, RedirectView
from django.views.generic.dates import (_date_from_string, _date_lookup_for_field,
                                        YearArchiveView, MonthArchiveView, DayArchiveView)
from django.views.generic.list import MultipleObjectMixin

from tagging.models import Tag, TaggedItem

from easy_blog.models import Config, Story


page_size = getattr(settings, "EASY_BLOG_PAGINATE_BY", 10)

class HomepageView(ListView):
    template_name = "easy_blog/homepage.html"

    def get_paginate_by(self, queryset):
        return Config.get_current().stories_in_index

    def get_queryset(self):
        if self.request.session.get("unpublished_on", False):
            kwargs = {"author": self.request.user, "status": [1,2,3]}
        else:
            kwargs = {"author": None, "status": [3]}
        stories = Story.objects.select(**kwargs).order_by("-pub_date")
        return stories
    

@login_required(redirect_field_name="")
def show_unpublished(request):
    redirect_to = request.REQUEST.get("next", '/')
    request.session["unpublished_on"] = True
    return HttpResponseRedirect(redirect_to)

@login_required(redirect_field_name="")
def hide_unpublished(request):
    redirect_to = request.REQUEST.get("next", '/')
    request.session["unpublished_on"] = False
    return HttpResponseRedirect(redirect_to)


class StoryDetailView(DateDetailView):
    def get_object(self, *args, **kwargs):
        qs = super(DateDetailView, self).get_object(*args, **kwargs)
        if qs.status > 2 and not qs.in_the_future:
            qs.visits = F('visits') + 1
            qs.save()
        return qs


class EasyBlogViewMixin(MultipleObjectMixin):
    def get_queryset(self):
        if self.request.session.get("unpublished_on", False):
            qs = self.model.objects.filter(status__in=[1,2,3]).exclude(
                ~Q(author=self.request.user), status=1)
            if not self.request.user.has_perm("easy_blog.can_review_posts"):
                qs = qs.exclude(~Q(author=self.request.user), status=2)
        else:
            qs = self.model.objects.filter(status=3, pub_date__lte=now())
        return qs.order_by("-pub_date")


class StoryListView(ListView, EasyBlogViewMixin):
    pass

class StoryDayArchiveView(DayArchiveView, EasyBlogViewMixin):
    date_field = "pub_date"
    make_object_list = True
    month_format = "%m"

class StoryMonthArchiveView(MonthArchiveView, EasyBlogViewMixin):
    date_field = "pub_date"
    make_object_list = True
    month_format = "%m"

class StoryYearArchiveView(YearArchiveView, EasyBlogViewMixin):
    date_field = "pub_date"
    make_object_list = True


class TagDetailView(ListView):
    """
    Paginated tag list

    Template: ``easy_blog/tag_detail.html``
    Context:
        object_list
            List of tags.
    """
    model = Tag
    slug_field = "name"
    template_name = "easy_blog/tag_detail.html"

    def get_paginate_by(self, queryset):
        return page_size

    def get_queryset(self):
        return TaggedItem.objects.filter(
            tag__name__iexact=self.kwargs.get("slug", "")).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        try:
            context["object"] = Tag.objects.get(name=self.kwargs.get("slug", ""))
        except Tag.DoesNotExist:
            raise Http404(_("Tag '%s' does not exist" % self.kwargs.get("slug", "")))
        return context
