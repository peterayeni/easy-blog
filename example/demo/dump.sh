python manage.py dumpdata --indent 4 --format json -v 2 \
    sites.Site \
    auth.User \
    easy_blog.Story \
    inline_media.InlineType \
    inline_media.PictureSet \
    inline_media.Picture \
    comments.Comment \
    django_comments_xtd.XtdComment \
    tagging.Tag \
    tagging.TaggedItem > initial_data.json

python manage.py dumpdata --indent 4 --format json -v 2 \
    easy_blog.Config \
    flatblocks.Flatblock > ../../easy_blog/fixtures/initial_data.json