#!/bin/bash

python manage.py syncdb --noinput
python manage.py migrate flatblocks
python manage.py migrate easy_blog
python manage.py migrate django_comments_xtd
python manage.py migrate inline_media
python manage.py loaddata fixtures/easy_blog.json
python manage.py loaddata fixtures/django_comments_xtd.json
python manage.py loaddata fixtures/flatblocks.json
python manage.py loaddata fixtures/example_data.json
python afterload.py
