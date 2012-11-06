#-*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import NoReverseMatch
from django.db import models
from django.test import TestCase as DjangoTestCase
from django.test.client import Client

from easy_blog.models import Story
from easy_blog.tests.utils import simple_story_dict

class StoryTestCase(DjangoTestCase):
    fixtures = ['sites.json', 'auth.json', 'config.json']

    def setUp(self):
        self.kwargs = simple_story_dict(User.objects.get(username="admin"))
        
    def test_body_markup_has_content(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        story = Story.objects.create(status=1, pub_date=tomorrow, 
                                     mod_date=tomorrow, **self.kwargs)
        self.assert_(len(story.body_markup) > 0)

    def test_get_draft_absolute_url(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        story = Story.objects.create(status=1, pub_date=tomorrow, 
                                     mod_date=tomorrow, **self.kwargs)
        url = story.get_absolute_url()
        # the result url contains the kwargs
        self.assert_(url.index("/%d/" % tomorrow.year) > -1)
        self.assert_(url.index("/%s/" % tomorrow.strftime("%b").lower()) > -1)
        self.assert_(url.index("/%d/" % tomorrow.day) > -1)
        self.assert_(url.index("/%s/" % story.slug) > -1)
        self.assert_(url.index("/draft/") > -1)

    def test_get_review_absolute_url(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        story = Story.objects.create(status=2, pub_date=tomorrow, 
                                     mod_date=tomorrow, **self.kwargs)
        url = story.get_absolute_url()
        self.assert_(url.index("/%d/" % tomorrow.year) > -1)
        self.assert_(url.index("/%s/" % tomorrow.strftime("%b").lower()) > -1)
        self.assert_(url.index("/%d/" % tomorrow.day) > -1)
        self.assert_(url.index("/%s/" % story.slug) > -1)
        self.assert_(url.index("/review/") > -1)

    def test_get_upcoming_absolute_url(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        story = Story.objects.create(status=3, pub_date=tomorrow, 
                                     mod_date=tomorrow, **self.kwargs)
        url = story.get_absolute_url()
        self.assert_(url.index("/%d/" % tomorrow.year) > -1)
        self.assert_(url.index("/%s/" % tomorrow.strftime("%b").lower()) > -1)
        self.assert_(url.index("/%d/" % tomorrow.day) > -1)
        self.assert_(url.index("/%s/" % story.slug) > -1)
        self.assert_(url.index("/upcoming/") > -1)

    def test_get_absolute_url(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        story = Story.objects.create(status=3, pub_date=yesterday, 
                                     mod_date=yesterday, **self.kwargs)
        url = story.get_absolute_url()
        self.assert_(url.index("/%d/" % yesterday.year) > -1)
        self.assert_(url.index("/%s/" % yesterday.strftime("%b").lower()) > -1)
        self.assert_(url.index("/%d/" % yesterday.day) > -1)
        self.assert_(url.index("/%s/" % story.slug) > -1)
        
    def test_in_the_future(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        story = Story.objects.create(status=3, pub_date=yesterday, 
                                     mod_date=yesterday, **self.kwargs)
        self.assertFalse(story.in_the_future)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        story = Story.objects.create(status=3, pub_date=tomorrow, 
                                     mod_date=tomorrow, **self.kwargs)
        self.assertTrue(story.in_the_future)
