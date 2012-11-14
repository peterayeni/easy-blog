#-*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import NoReverseMatch
from django.db import models
from django.test import TestCase as DjangoTestCase
from django.test.client import Client

from easy_blog.models import Config, Story


class StoryTestCase(DjangoTestCase):
    fixtures = ['sites.json', 'auth.json', 'config.json']

    def setUp(self):
        self.kwargs = {
            'title': "Short title for a testing story",
            'slug': "short-title-for-testing-story",
            'body': "This is the content of the story.", 
            'tags': "mobile vikings",
            'author': User.objects.get(username="admin"),
            'allow_comments': True,
            'site': Config.get_current().site }
        self.tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        
    def test_body_has_content(self):
        story = Story.objects.create(status=1, pub_date=self.tomorrow, 
                                     mod_date=self.tomorrow, **self.kwargs)
        self.assert_(len(story.body) > 0)

    def test_get_draft_absolute_url(self):
        story = Story.objects.create(status=1, pub_date=self.tomorrow, 
                                     mod_date=self.tomorrow, **self.kwargs)
        url = story.get_absolute_url()
        self.assert_(url.index("/draft/") > -1)
        # response redirect when author is not logged in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # ok when author is logged in
        self.assertTrue(self.client.login(username="admin", password="admin"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_review_absolute_url(self):
        # bob cannot review other people stories, so accessing will be redirected
        user_bob   = User.objects.create_user("bob", "bob@example.com", "admin")
        # alice will have can_review_stories permission, so she will have access
        user_alice = User.objects.create_user("alice", "alice@example.com", "admin")
        ct_story = ContentType.objects.get(app_label="easy_blog", model="story")
        can_review_stories = Permission.objects.get(content_type=ct_story, 
                                                    codename="can_review_stories")
        user_alice.user_permissions.add(can_review_stories)
        user_alice.save()
        self.assertTrue(user_alice.has_perm("easy_blog.can_review_stories"))
        # create story in review mode
        story = Story.objects.create(status=2, pub_date=self.tomorrow, 
                                     mod_date=self.tomorrow, **self.kwargs)
        url = story.get_absolute_url()
        self.assert_(url.index("/review/") > -1)
        # response redirect when author is not logged in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # or when author is logged in but has not the "can_review_stories" permission
        self.assertTrue(self.client.login(username="bob", password="admin"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        # Alice has "can_review_stories" permission
        import ipdb; ipdb.set_trace()
        self.assertTrue(self.client.login(username="alice", password="admin"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

