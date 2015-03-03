from setuptools import setup, find_packages
from setuptools.command.test import test

def run_tests(*args):
    from easy_blog.tests import run_tests
    run_tests()

test.run_tests = run_tests

setup(
    name = "django-easy-blog",
    version = "0.1a",
    packages = find_packages(),
    keywords = "django apps",
    license = "MIT",
    description = "Django blogging app with stories, comments, tags and search, that uses the Wysihtml5 rich text editor, and will suit your mixed profile team of bloggers.",
    long_description = "Easy to use Django blogging application with stories, comments, tags, search capabilities, multi-author support, draft/review modes and in-future posts, that allows authors to write content with the simple easy to use rich-text editor Wysihtml5.",
    author = "Daniel Rus Morales",
    author_email = "inbox@danir.us",
    maintainer = "Daniel Rus Morales",
    maintainer_email = "inbox@danir.us",
    url = "http://pypi.python.org/pypi/django-easy-blog/",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    include_package_data = True,
    test_suite = "dummy",
    install_requires = [
        'django-contrib-comments>=1.5',
    ]
)
