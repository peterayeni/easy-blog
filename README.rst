Django-easy-blog
================

This project was initiated and supported by `Mobile Vikings <http://www.mobilevikings.com>`_.

By `Daniel Rus Morales <http://github.com/danirus/>`_ and `Kristof Houben <http://github.com/kristof/>`_.

* http://pypi.python.org/pypi/django-easy-blog/
* http://github.com/citylive/django-easy-blog/

Yet another Django pluggable blogging app that features:

1. Stories with inline media content like Pictures and PictureSets.
1. Comments with threads, email confirmation and follow up notifications.
2. No need to know markup languages as it uses the rich text editor Wysihtml5.
3. But if you want to use markup languages like Markdown or reStructuredText you can.
4. Posts may be in Draft/Public status, and published in the future.
5. Support for multiple authors.
6. Posts categorized with tags.
7. Search capabilities.

Documentation work in progress, so far the list of features and a screenshot:

* `Read The Docs`_
* `Python Packages Site`_

.. _`Read The Docs`: http://readthedocs.org/docs/django-easy-blog/
.. _`Python Packages Site`: http://packages.python.org/django-easy-blog/

Install the app and run the example site to see it in action:

1. Create a VirtualEnv for the app
2. Git clone: `git clone git://github.com/citylive/django-easy-blog.git`
3. Cd into `django-easy-blog` and install requirements: `pip install requirements`
4. To have search functionality up & running:
    * Install Xapian >= 1.2, and
    * Copy: `cp ../src/xapian-haystack/xapian_backend.py ../src/django-haystack/haystack/backends/`
5. If you don't want to have search at the moment just edit `django-easy-blog/example/demo/settings.py` and comment out `"haystack"` in `INSTALLED_APPS`
6. Cd into `django-easy-blog/example/demo`
7. Run `python manage.py collectstatic`, and answer 'yes'
8. Run `sh install.sh` (to syncdb, migrate and loaddata)
9. If you have installed xapian, build the search index:
    * `python manage.py rebuild_index`
10. Run `python manage.py localhost` and hit http://localhost:8000

Admin access with user **admin**, password **admin**.
