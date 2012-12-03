#!/usr/bin/env python

import imp
import sys
import os
import os.path

PRJ_PATH = os.path.abspath(os.path.curdir)
PARENT_PRJ_PATH = os.path.abspath(os.path.join(PRJ_PATH, os.pardir))
APP_PATH = os.path.abspath(os.path.join(PARENT_PRJ_PATH, os.pardir))

sys.path.insert(0, APP_PATH)
sys.path.insert(0, PARENT_PRJ_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'

try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from tagging.models import TaggedItem
from easy_blog.models import Story
from django_comments_xtd.models import XtdComment
from sorl.thumbnail import get_thumbnail
from inline_media.models import Picture 

from easy_blog.auth import initialize_groups

def setup_users():
    """Create the 'Blog Authors' group, assign 'Can review stories' to alice.

    3 users: admin, alice, bob
    All them belong to 'Blog Authors' group.
    Alice has extra rights: she has 'can_review_stories' permission.
    """
    # story_ct = ContentType.objects.filter(app_label="easy_blog", model="story")
    # can_review_per = Permission.objects.get(content_type=story_ct, codename="can_review_stories")
    blog_authors_grp, blog_reviewers_grp = initialize_groups()
    admin = User.objects.get(username="admin")
    alice = User.objects.get(username="alice")
    bob = User.objects.get(username="bob")
    # blog authors group
    # blog_authors_grp = Group.objects.create(name="Blog Authors")
    # for per in Permission.objects.filter(content_type=story_ct):
    #     if per != can_review_per:
    #         blog_authors_grp.permissions.add(per)
    blog_authors_grp.user_set.add(admin, alice, bob)
    blog_authors_grp.save()
    # blog reviewers group
    # blog_reviewers_grp = Group.objects.create(name="Blog Reviewers")
    # blog_reviewers_grp.permissions.add(can_review_per)
    blog_reviewers_grp.user_set.add(alice)
    blog_reviewers_grp.save()


def fix_content_types():
    """Fix content type attributes of dress_blog instances.

    easy_blog models' instances may have wrong content type values
    as a result of loading the fixture. This may happen during the
    schema creation when creating the database for the demo project.
    """
    # fix content type for stories
    story_ct = ContentType.objects.get_for_model(Story)
    for story in Story.objects.all():
        story.content_type = story_ct
        story.save()

    # fix content type for xtdcomments
    for xtdcomment in XtdComment.objects.all():
        if xtdcomment.id in range(1, 11):
            xtdcomment.content_type = diarydetail_ct
        elif xtdcomment.id in [11, 12]:
            xtdcomment.content_type = quote_ct
        elif xtdcomment.id == 13:
            xtdcomment.content_type = story_ct
        xtdcomment.save()
        
def fix_tagged_items():
    story_ct = ContentType.objects.get_for_model(Story)
    picture_ct = ContentType.objects.get_for_model(Picture)
    for ti in TaggedItem.objects.all():
        if not ti.content_type in [Story, Picture]:
            if ti.id < 16:
                ti.content_type = story_ct
            else:
                ti.content_type = picture_ct
            ti.save()


if __name__ == '__main__':
    setup_users()
    fix_content_types()
    fix_tagged_items()
