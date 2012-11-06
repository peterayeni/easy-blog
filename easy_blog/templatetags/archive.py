#-*- coding: utf-8 -*-

import re

from django import template

from easy_blog.models import Story


register = template.Library()


class StoryArchive(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        dates = Story.objects.published().dates("pub_date", "month", 
                                                order='DESC')
        if dates:
            context[self.var_name] = dates
        return ''

@register.tag
def get_story_archive(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return StoryArchive(var_name)


class PopularStories(template.Node):
    def __init__(self, count, as_varname):
        try:
            self.count = int(count)
        except:
            self.count = Variable(count)
        self.as_varname = as_varname

    def render(self, context):
        stories = Story.objects.published().order_by('-visits')[:self.count]
        if stories and (self.count == 1):
            context[self.as_varname] = stories[0]
        else:
            context[self.as_varname] = stories
        return ''

@register.tag
def get_popular_stories(parser, token):
    """
    Get the most popular N stories and store them in a variable.

    Syntax::

        {% get_popular_stories [N] as [var_name] %}

    Example usage::

        {% get_popular_stories 10 as popular_story_list %}
    """
    tokens = token.contents.split()

    try:
        count = int(tokens[1])
    except ValueError:
        raise TemplateSyntaxError(
            "Second argument in %r tag must be a integer" % tokens[0])

    if tokens[2] != 'as':
        raise TemplateSyntaxError(
            "Third argument in %r tag must be 'as'" % tokens[0])

    as_varname = tokens[3]

    return PopularStories(count, as_varname)

    
