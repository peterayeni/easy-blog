from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.core.urlresolvers import reverse

from inline_media.parser import inlines
from tagging.models import Tag, TaggedItem

from easy_blog.models import Config, Story


ct_story = ContentType.objects.get(app_label="easy_blog", model="story")


class LatestStoriesFeed(Feed):
    _config = None
    
    @property
    def config(self):
        if self._config is None:
            self._config = Config.get_current()
        return self._config

    def item_pubdate(self, item):
        return item.pub_date

    def item_title(self, item):
        child = getattr(item, item.content_type.model)
        return child.title

    def item_link(self, item):
        child = getattr(item, item.content_type.model)
        return child.get_absolute_url()

    def item_description(self, item):
        child = getattr(item, item.content_type.model)
        return inlines(child.body)

    def item_author_name(self, item):
        child = getattr(item, item.content_type.model)
        return child.author.get_full_name()       

    def title(self):
        return '%s stories feed' % self.config.title

    def description(self):
        return '%s latest stories feed.' % self.config.title

    def link(self):
        return reverse('blog-story-list')

    def items(self):
        return Story.objects.published()[:10]


class PostsByTag(Feed):
    _config = None
    
    @property
    def config(self):
        if self._config is None:
            self._config = Config.get_current()
        return self._config

    def get_object(self, request, slug):
        if not slug:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__exact=slug)

    def title(self, obj):
        return ur'''%s posts tagged as '%s' feed''' % (self.config.title, obj.name)

    def description(self):
        return ur'''%s latest posts tagged as '%s' feed.''' % (self.config.title, obj.name)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('blog-tag-detail', None, {"slug": obj.name})

    def feed_url(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('posts-tagged-as', None, {"slug": obj.name})

    def description(self, obj):
        return "Posts tagged as %s" % obj.name
    
    def items(self, obj):
        return TaggedItem.objects.filter(
            tag__name__iexact=obj.name,
            content_type__in=[ct_story,]).order_by("-id")[:10]

    def item_pubdate(self, item):
        return item.object.pub_date

    def item_title(self, item):
        return item.object.title

    def item_link(self, item):
        return item.object.get_absolute_url()

    def item_description(self, item):
        return inlines(item.object.body)

    def item_author_name(self, item):
        return item.object.author.get_full_name()       
