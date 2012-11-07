#-*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.db import models
try:
    from django.utils.timezone import now
except ImportError:
    from easy_blog.utils import now

import re

Story = models.get_model('easy_blog', 'story')

register = template.Library()

class EasyBlogBaseTemplateNode(template.Node):
    def __init__(self, limit, var_name):
        try:
            self.limit = int(limit)
        except:
            self.limit = template.Variable(limit)
        self.var_name = var_name
        
    def get_queryset(self, context):
        return None
    
    def render(self, context):
        if not isinstance(self.limit, int):
            self.limit = int( self.limit.resolve(context) )

        queryset = self.get_queryset(context)
        if queryset:
            context[self.var_name] = queryset
        return ''

def easy_blog_base_tag(parser, token):
    """Generic tag: {% tag_name [limit] as [var_name] %}"""
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return (format_string, var_name)

#------------------------------------------------------------------------
class LatestStories(EasyBlogBaseTemplateNode):
    def get_queryset(self, context):
        if context["request"].session.get("unpublished_on", False):
            qs = Story.objects.filter(status__in=[1,2,3]).exclude(
                ~models.Q(author=context["request"].user), status=1)
            if not context["request"].user.has_perm("easy_blog.can_review_posts"):
                qs = qs.exclude(~Q(author=context["request"].user), status=2)
        else:
            qs = Story.objects.filter(status=3, pub_date__lte=now())
        return qs[:self.limit]

@register.tag
def get_latest_stories(parser, token):
    return LatestStories(*easy_blog_base_tag(parser, token))

#----------
class DraftStories(EasyBlogBaseTemplateNode):
    def get_queryset(self, context):
        user = template.Variable("user").resolve(context)            
        return Story.objects.drafts(user)[:self.limit]

@register.tag
def get_draft_stories(parser, token):
    return DraftStories(*easy_blog_base_tag(parser, token))

#----------
class ReviewStories(EasyBlogBaseTemplateNode):
    def get_queryset(self, context):
        user = template.Variable("user").resolve(context)            
        return Story.objects.reviews(user)[:self.limit]

@register.tag
def get_review_stories(parser, token):
    return ReviewStories(*easy_blog_base_tag(parser, token))
