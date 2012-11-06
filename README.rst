Django-easy-blog
================

This project was initiated and supported by `Mobile Vikings <http://www.mobilevikings.com>`_.

By `Daniel Rus Morales <http://github.com/danirus/>`_ and `Kristof Houben <http://github.com/kristof/>`_.

* http://pypi.python.org/pypi/django-easy-blog/
* http://github.com/citylive/django-easy-blog/

Yet another Django pluggable blogging app that features:

1. Stories with inline media content like Pictures and PictureSets.
2. Comments with threads, email confirmation and follow up notifications.
3. No need to know markup languages as it uses the rich text editor Wysihtml5.
4. But if you want to use markup languages like Markdown or reStructuredText you can.
5. Posts may be in Draft/Public status, and published in the future.
6. Support for multiple authors.
7. Posts categorized with tags.
8. Search capabilities.

Documentation work in progress, so far the list of features and a screenshot:

* `Read The Docs`_
* `Python Packages Site`_

.. _`Read The Docs`: http://readthedocs.org/docs/django-easy-blog/
.. _`Python Packages Site`: http://packages.python.org/django-easy-blog/

Includes a **demo site** and a limited **test suite**. If you commit code, please consider adding proper coverage (especially if it has a chance for a regression) in the test suite.

Run the tests with:  ``python setup.py test``.

To have search functionality up & running:

1. Install Xapian >= 1.2, and
2. Copy: `cp ../src/xapian-haystack/xapian_backend.py ../src/django-haystack/haystack/backends/`

Install the app and run the example site to see it in action:

1. Create a VirtualEnv for the app.
2. Git clone: `git clone git://github.com/citylive/django-easy-blog.git`.
3. Cd into `django-easy-blog` and install requirements: `pip install requirements`.
4. If you don't want to have search at the moment just edit `django-easy-blog/example/demo/settings.py` and comment out `"haystack"` in `INSTALLED_APPS`
5. Cd into `django-easy-blog/example/demo`
6. Run `python manage.py collectstatic`, and answer 'yes'
7. Run `sh install.sh` (to syncdb, migrate and loaddata)
8. If you have installed xapian, build the search index: `python manage.py rebuild_index`
9. Run `python manage.py localhost` and hit http://localhost:8000

Demo admin access with user **admin**, password **admin**.
