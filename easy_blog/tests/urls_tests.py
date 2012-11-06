#-*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase as DjangoTestCase

from easy_blog.models import Story
from easy_blog.tests.utils import (simple_story_dict, setup_group_blog_authors, 
                                   give_permission_to_review_stories)


class StoryURLsTestCase(DjangoTestCase):
    fixtures = ['sites.json', 'auth.json', 'config.json']
    
    def setUp(self):
        self.kwargs = simple_story_dict(User.objects.get(username="admin"))

    def test_url_blog_story_detail_month_numeric(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        story = Story.objects.create(status=3, pub_date=yesterday, 
                                     mod_date=yesterday, **self.kwargs)
        url = reverse("blog-story-detail-month-numeric", 
                      kwargs={"year": yesterday.year,
                              "month": yesterday.month,
                              "day": yesterday.day,
                              "slug": story.slug})
        # the result url contains the kwargs
        self.assert_(url.index("/%d/" % yesterday.year) > -1)
        self.assert_(url.index("/%d/" % yesterday.month) > -1)
        self.assert_(url.index("/%d/" % yesterday.day) > -1)
        self.assert_(url.index("/%s/" % story.slug) > -1)
        # the corresponding view is getting the request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_blog_story_detail(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        story = Story.objects.create(status=3, pub_date=yesterday, 
                                     mod_date=yesterday, **self.kwargs)
        url = story.get_absolute_url()
        # the result url contains the kwargs
        self.assert_(url.index("/%d/" % yesterday.year) > -1)
        self.assert_(url.index("/%s/" % yesterday.strftime("%b").lower()) > -1)
        self.assert_(url.index("/%d/" % yesterday.day) > -1)
        self.assert_(url.index("/%s/" % story.slug) > -1)
        # the corresponding view is getting the request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_blog_story_detail_draft(self):
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
        # response redirect when author is not logged in
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # ok when uswer belongs to group 'Blog Authors'
        self.assertTrue(self.client.login(username="admin", password="admin"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_url_blog_story_detail_review(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        # bob cannot review other people stories, so he will be redirected
        user_bob   = User.objects.create_user("bob", "bob@example.com", "admin")
        # alice will have can_review_stories permission, so she will get a 200
        user_alice = User.objects.create_user("alice", "alice@example.com", "admin")
        give_permission_to_review_stories(user_alice)
        # create story in review mode
        story = Story.objects.create(status=2, pub_date=tomorrow, 
                                     mod_date=tomorrow, **self.kwargs)
        url = story.get_absolute_url()
        # the result url contains the kwargs
        self.assert_(url.index("/%d/" % tomorrow.year) > -1)
        self.assert_(url.index("/%s/" % tomorrow.strftime("%b").lower()) > -1)
        self.assert_(url.index("/%d/" % tomorrow.day) > -1)
        self.assert_(url.index("/%s/" % story.slug) > -1)
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
        self.assertTrue(self.client.login(username="alice", password="admin"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_url_blog_story_detail_upcoming(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        # users in the 'Blog Authors' group can see upcoming stories
        user_anonymous = User.objects.create_user("someone", "someone@example.com", "admin")
        user_bob = User.objects.create_user("bob", "bob@example.com", "admin")
        setup_group_blog_authors(user_bob)
        # create story in public mode, set pub_date in future
        story = Story.objects.create(status=3, pub_date=tomorrow, 
                                     mod_date=tomorrow, **self.kwargs)
        url = story.get_absolute_url()
        # the result url contains the kwargs
        self.assert_(url.index("/%d/" % tomorrow.year) > -1)
        self.assert_(url.index("/%s/" % tomorrow.strftime("%b").lower()) > -1)
        self.assert_(url.index("/%d/" % tomorrow.day) > -1)
        self.assert_(url.index("/%s/" % story.slug) > -1)
        self.assert_(url.index("/upcoming/") > -1)
        # the story URL is not accessible for non-logged in users
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # and neither users who don't belong to group 'Blog Authors' can see the story URL
        self.assertTrue(self.client.login(username="someone", password="admin"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        # Bob belongs to 'Blog Authors' so he can see this upcoming story
        self.assertTrue(self.client.login(username="bob", password="admin"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
 
    def test_url_blog_story_archive_day(self):
        today = datetime.datetime.now()
        story = Story.objects.create(status=3, pub_date=today, 
                                     mod_date=today, **self.kwargs)
        url = reverse("blog-story-archive-day", 
                      kwargs={"year": today.year,
                              "month": today.month,
                              "day": today.day})
        # the result url contains the kwargs
        self.assert_(url.index("/%d/" % today.year) > -1)
        self.assert_(url.index("/%d/" % today.month) > -1)
        self.assert_(url.index("/%d/" % today.day) > -1)
        # the corresponding view is getting the request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_url_blog_story_archive_month(self):
        today = datetime.datetime.now()
        story = Story.objects.create(status=3, pub_date=today, 
                                     mod_date=today, **self.kwargs)
        url = reverse("blog-story-archive-month", 
                      kwargs={"year": today.year,
                              "month": today.month})
        # the result url contains the kwargs
        self.assert_(url.index("/%d/" % today.year) > -1)
        self.assert_(url.index("/%d/" % today.month) > -1)
        # the corresponding view is getting the request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_blog_story_archive_year(self):
        today = datetime.datetime.now()
        story = Story.objects.create(status=3, pub_date=today, 
                                     mod_date=today, **self.kwargs)
        url = reverse("blog-story-archive-year", 
                      kwargs={"year": today.year})
        # the result url contains the kwargs
        self.assert_(url.index("/%d/" % today.year) > -1)
        # the corresponding view is getting the request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_blog_story_list(self):
        today = datetime.datetime.now()
        story = Story.objects.create(status=3, pub_date=today, 
                                     mod_date=today, **self.kwargs)
        url = reverse("blog-story-list") 
        # the corresponding view is getting the request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
