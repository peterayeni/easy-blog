#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from easy_blog.auth import initialize_groups, blog_authors_group_name


class BlogAuthorsListFilter(SimpleListFilter):
    # the title for the filter
    title = _("Blog authors")

    # parameter name for the url
    parameter_name = "author"


    # A list of tuples, the first element is what appears in the URL, and
    # the second element is the human readable part that you read in the
    # filters block
    def lookups(self, request, model_admin):
        authors_group = None
        try:
            authors_group = Group.objects.get(name=blog_authors_group_name)
        except Group.DoesNotExist:
            authors_group = initialize_groups()[0]

        return map(lambda u: (u.username, u.get_full_name()),  
                   User.objects.filter(groups__in=[authors_group]))


    # Returns the filtered queryset based on the value provided in the
    # query string and retrievable via self.value()
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__username=self.value())
