#-*- coding: utf-8 -*-

import os.path

from django.db import models
from django.db.models import permalink, Q
from django.db.models.signals import post_delete
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.text import truncate_words
try:
    from django.utils.timezone import now
except ImportError:
    from easy_blog.utils import now
from django.utils.translation import ugettext, ugettext_lazy as _

from django_markup.fields import MarkupField
from django_markup.markup import formatter
from inline_media.fields import TextFieldWithInlines
from inline_media.utils import unescape_inline
from tagging.fields import TagField
from tagging.models import TaggedItem
from tagging.utils import get_tag_list

from easy_blog.utils import create_cache_key, colloquial_date


class DefaultConfig(object):
    def __init__(self, data=None):
        self.data = data
    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None
        

default_config = DefaultConfig(
    getattr(
        settings, "EASY_BLOG_DEFAULT_CONFIG", 
        { "site": 1,
          "title": u"Your Easy Blog",
          "stories_in_index": 5,
          "comments_in_index": 2,
          "email_subscribe_url": u"",
          "show_author": True,
          "ping_google": False,
          "excerpt_length": 500,
          "meta_author": u"",
          "meta_keywords": u"",
          "meta_description": u""}))
                               

STATUS_CHOICES = ((1, _("Draft")), (2, _("Review")), (3, _("Public")),)


class Config(models.Model):
    """Django-easy-blog configuration"""

    site = models.ForeignKey(Site, unique=True, related_name="+")
    title = models.CharField(max_length=100, help_text=_(
            "Blog's name or title"))
    stories_in_index = models.IntegerField(default=5, help_text=_(
            "List of stories in the front page."))
    comments_in_index = models.IntegerField(default=5, help_text=_(
            "List of last comments in the front page."))
    email_subscribe_url = models.URLField(_("subscribe via email url"), 
                                          blank=True, null=True)
    show_author = models.BooleanField(default=False, help_text=_(
            "Show author's full name along in posts"))
    ping_google = models.BooleanField(default=False, help_text=_(
            "Notify Google on new submissions"))
    excerpt_length = models.IntegerField(default=500, help_text=_(
            "The character length of the post body field displayed in RSS "
            "and preview templates."))
    meta_author = models.CharField(max_length=255, help_text=_(
            "List of authors or company/organization's name"))
    meta_keywords = models.CharField(max_length=255, help_text=_(
            "List of keywords to help improve quality of search results"))
    meta_description = models.TextField(blank=True, help_text=_(
            "What the blog is about, topics, editorial line..."))
    
    class Meta:
        db_table = "easy_blog_config"
        verbose_name = _("app config")
        verbose_name_plural = _("app config")

    def __unicode__(self):
        return "%s easy-blog config" % self.site.name

    def delete(self, *args, **kwargs):
        if settings.SITE_ID != self.site.id:
            super(Config, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Config, self).save(*args, **kwargs)
        self.site_name = self.site.name
        key = create_cache_key(Config, field="site__id", 
                               field_value=self.site.id)
        cache.set(key, self)

    @staticmethod
    def get_current():
        site = Site.objects.get_current()
        key = create_cache_key(Config, field="site__id", 
                               field_value=site.id)
        config = cache.get(key, None)
        if config is None:
            try:
                config = Config.objects.get(site=site)
                cache.add(key, config)
            except Config.DoesNotExist:
                return default_config
        return config


class StoryManager(models.Manager):
    """Returns published posts that are not in the future."""
    
    def drafts(self, author=None):
        if not author:
            return self.get_query_set().filter(
                status=1).order_by("-mod_date")
        else:
            return self.get_query_set().filter(
                status=1, author=author).order_by("-mod_date")

    def reviews(self, author):
        if author.has_perm("easy_blog.can_review_posts"):
            return self.get_query_set().filter(status=2).order_by("-mod_date")
        else:
            return []

    def upcoming(self, author=None):
        if not author:
            return self.get_query_set().filter(
                status=3, pub_date__gt=now()).order_by("-mod_date")
        else:
            return self.get_query_set().filter(
                status=3, author=author, pub_date__gt=now()).order_by("-mod_date")

    def published(self):
        return self.get_query_set().filter(status=3, pub_date__lte=now())

    def select(self, status=[3], author=None):
        if min(status) < 3 and author: # show drafts anf reviews for the author
            qs = self.get_query_set().filter(
                status__in=status).exclude(~Q(author=author), status=1)
            if not author.has_perm("dress_blog.can_review_posts"):
                return qs.exclude(~Q(author=author), status=2)
            else:
                return qs
        else:
            return self.get_query_set().filter(
                status__in=status, pub_date__lte=now())


_htxt = {'markup_text': u'Check <a href="http://markable.in/file/aa191728-9dc7-11e1-91c7-984be164924a/" target=_new">Markdown syntax</a>, <a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target=_new">reStructuredText syntax</a>',
         'site': _("Site in which the entry is published"),
         'hint_on_markdown': _("Look at the body field for a quick Markdown cheatsheet"),
         'markdown_cheatsheet': u'''
In case you need to write headers to highlight different sections along the story, you can use headers like the following.

### Header Level 3

This is a paragraph with simple content, not too long and too short, just enough to make it look like a paragraph. **This sentence has a font in bold**. *And this is in italics*. A markdown link looks like this: [Link to Google](http://www.google.com). But use HTML links at will too, specially when you want them to be opened in a different window: <A href="http://www.google.com" target="_new">Google in a new window</a>.

<div style="margin:10px auto;text-align:center">Paste here your youtube or google docs content</div>

This is a regular list:

* The first element of the list
* The second element of the list
* The third element of the list

And this a numbered list:

1. The first
1. The second
1. The third

Remember, you can separate paragraphs with horizontal rules, by simply typing three asterisks.

***

So this paragraph will be below a horizontal rule.

If you want to quote a text, as when you make a citation, use the following:
> A small step for man a giant leap for mankind.

Enjoy markdown!
'''}

class Story(models.Model):
    """A generic story."""
    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique_for_date="pub_date")
    markup          = MarkupField(default="markdown")
    abstract        = TextFieldWithInlines(help_text=_htxt["markup_text"],
                                           default=_htxt["hint_on_markdown"])
    abstract_markup = models.TextField(editable=True, blank=True, null=True)
    body            = TextFieldWithInlines(help_text=_htxt["markup_text"],
                                           default=_htxt["markdown_cheatsheet"])
    body_markup     = models.TextField(editable=True, blank=True, null=True)
    tags            = TagField()
    status          = models.IntegerField(choices=STATUS_CHOICES, default=1)
    author          = models.ForeignKey(User, blank=True, null=True)
    allow_comments  = models.BooleanField(default=True)
    pub_date        = models.DateTimeField(_("Publication date"), default=now)
    mod_date        = models.DateTimeField(_("Modification date"), auto_now=True)
    visits          = models.IntegerField(default=0, editable=False)
    site            = models.ForeignKey(Site, help_text=_htxt['site'])
    objects         = StoryManager()

    class Meta:
        verbose_name = _("story")
        verbose_name_plural = _("stories")
        db_table  = "easy_blog_stories"
        ordering  = ("-pub_date",)
        get_latest_by = "pub_date"
        permissions = (("can_review_stories", "Can review stories"),
                       ("can_see_unpublished_stories", "Can see unpublished stories"))

    def __unicode__(self):
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        self.site_id = settings.SITE_ID
        self.abstract_markup = mark_safe(
            formatter(self.abstract, filter_name=self.markup))
        self.body_markup = mark_safe(
            formatter(self.body, filter_name=self.markup))
        if self.markup == "restructuredtext":
            self.abstract_markup = unescape_inline(self.abstract_markup)
            self.body_markup = unescape_inline(self.body_markup)
        super(Story, self).save(*args, **kwargs)
        if self.status == 3: # public
            blog_config = Config.get_current()
            ping_google = getattr(blog_config, "ping_google", False) 
            if ping_google:
                try:
                    ping_google()
                except:
                    pass

    @permalink
    def get_absolute_url(self):
        kwargs = { "year": self.pub_date.year,
                   "month": self.pub_date.strftime("%b").lower(),
                   "day": self.pub_date.day,
                   "slug": self.slug }

        if self.status == 1:
            return ("blog-story-detail-draft", None, kwargs)
        if self.status == 2:
            return ("blog-story-detail-review", None, kwargs)
        elif self.pub_date > now():
            return ("blog-story-detail-upcoming", None, kwargs)
        else:
            return ("blog-story-detail", None, kwargs)

    @property
    def in_the_future(self):
        return self.pub_date > now()


def delete_story_tags(sender, instance, **kwargs):
    try:
        ctype = ContentType.objects.get_for_model(instance)
        tags = get_tag_list(instance.tags)
        TaggedItem._default_manager.filter(content_type__pk=ctype.pk,
                                           object_id=instance.pk,
                                           tag__in=tags).delete()
        for tag in tags:
            if not tag.items.count():
                tag.delete()
    except Exception, e:
        # let 'django.request' logger handle the exception
        raise e

post_delete.connect(delete_story_tags, sender=Story)
