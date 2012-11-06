#-*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from easy_blog.models import Config


def setup_group_blog_authors(*users):
    """Initialize group 'Blog Authors' with users given as arguments."""
    story_ct = ContentType.objects.filter(app_label="easy_blog", model="story")
    can_see_unpub_per = Permission.objects.get(content_type=story_ct, 
                                               codename="can_see_unpublished_stories")
    blog_authors_grp = Group.objects.create(name="Blog Authors")
    blog_authors_grp.permissions.add(can_see_unpub_per)
    blog_authors_grp.user_set.add(*users)
    blog_authors_grp.save()


def give_permission_to_review_stories(*users):
    """Give permission 'can_review_stories' to the users given as arguments."""
    ct_story = ContentType.objects.get(app_label="easy_blog", model="story")
    can_review_stories = Permission.objects.get(content_type=ct_story, 
                                                codename="can_review_stories")
    for user in users:
        user.user_permissions.add(can_review_stories)
        user.save()


def simple_story_dict(user):
    return {
        'title': "Short title for a testing story",
        'slug': "short-title-for-testing-story",
        'markup': "markdown",
        'body': "This is a [link](http://www.mobilevikings.com) written\
 in Markdown to Mobile Vikings website", 
        'tags': "mobile vikings",
        'author': user,
        'allow_comments': True,
        'site': Config.get_current().site
    }
