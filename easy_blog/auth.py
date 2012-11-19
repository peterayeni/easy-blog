#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


blog_authors_group_name = getattr(
    settings, "EASY_BLOG_AUTHORS_GROUP_NAME", "Blog Authors")

blog_reviewers_group_name = getattr(
    settings, "EASY_BLOG_REVIEWERS_GROUP_NAME", "Blog Reviewers")


def initialize_groups():
    story_ct = ContentType.objects.filter(app_label="easy_blog", model="story")
    can_review_per = Permission.objects.get(content_type=story_ct, codename="can_review_stories")

    # blog authors group
    blog_authors_grp = Group.objects.create(name=blog_authors_group_name)
    for per in Permission.objects.filter(content_type=story_ct):
        if per != can_review_per:
            blog_authors_grp.permissions.add(per)
    blog_authors_grp.save()

    # blog reviewers group
    blog_reviewers_grp = Group.objects.create(name=blog_reviewers_group_name)
    blog_reviewers_grp.permissions.add(can_review_per)
    blog_reviewers_grp.save()

    return (blog_authors_grp, blog_reviewers_grp)
