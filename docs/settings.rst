.. _ref-settings:

========
Settings
========

Django-easy-blog recognizes the following settings:


.. index::
   single: EASY_BLOG_DEFAULT_CONFIG
   pair: Setting; EASY_BLOG_DEFAULT_CONFIG

``EASY_BLOG_DEFAULT_CONFIG``
============================

**Optional**

This setting establishes default configuration values for the blog app. It will be used just in case there is no ``easy_blog.models.Config`` instance associated with the Site.get_current() site.

The value of EASY_BLOG_DEFAULT_CONFIG is a dictionary with default values for several blog attributes, like the title, how many stories should list the blog homepage, how many comments, whether to show the author along with the story title, etc.

Example with the values the setting defaults to::

    EASY_BLOG_DEFAULT_CONFIG = {
        "site": 1,
        "title": u"Your Easy Blog",
        "stories_in_index": 5,
        "comments_in_index": 2,
        "email_subscribe_url": u"",
        "show_author": True,
        "ping_google": False,
        "excerpt_length": 500,
        "meta_author": u"",
        "meta_keywords": u"",
        "meta_description": u""
    }


.. index::
   single: EASY_BLOG_AUTHORS_GROUP_NAME
   pair: Setting; EASY_BLOG_AUTHORS_GROUP_NAME

``EASY_BLOG_AUTHORS_GROUP_NAME``
================================

**Optional**

This setting establishes the name of the Django auth group for blog authors. Users who write blog stories should belong to this group.

An example::

    EASY_BLOG_AUTHORS_GROUP_NAME = "Blog Authors"

Defaults to ``Blog Authors``.


.. index::
   single: EASY_BLOG_AUTHORS_GROUP_NAME
   pair: Setting; EASY_BLOG_AUTHORS_GROUP_NAME

``EASY_BLOG_REVIEWERS_GROUP_NAME``
==================================

**Optional**

This setting establishes the name of the Django auth group for blog reviewers. Users with access to stories in **review mode** should belong to this group.

An example::

    EASY_BLOG_REVIEWERS_GROUP_NAME = "Blog Reviewers"

Defaults to ``Blog Reviewers``.
