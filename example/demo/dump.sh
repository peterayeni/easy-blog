#!/bin/bash

python manage.py dumpdata --indent 4 --format json -v 2 \
    easy_blog.Config \
    easy_blog.Story > fixtures/easy_blog.json

python manage.py dumpdata --indent 4 --format json -v 2 \
    comments.Comment \
    django_comments_xtd.XtdComment > fixtures/django_comments_xtd.json

python manage.py dumpdata --indent 4 --format json -v 2 \
    flatblocks.Flatblock > fixtures/flatblocks.json

python manage.py dumpdata --indent 4 --format json -v 2 \
    sites.Site \
    auth.User \
    inline_media.InlineType \
    inline_media.PictureSet \
    inline_media.Picture \
    tagging.Tag \
    tagging.TaggedItem > fixtures/example_data.json
