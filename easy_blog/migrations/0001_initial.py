# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import inline_media.fields
import django_markup.fields
import django.utils.timezone
from django.conf import settings
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text="Blog's name or title", max_length=100)),
                ('stories_in_index', models.IntegerField(default=5, help_text='List of stories in the front page.')),
                ('comments_in_index', models.IntegerField(default=5, help_text='List of last comments in the front page.')),
                ('email_subscribe_url', models.URLField(null=True, verbose_name='subscribe via email url', blank=True)),
                ('show_author', models.BooleanField(default=False, help_text="Show author's full name along in posts")),
                ('ping_google', models.BooleanField(default=False, help_text='Notify Google on new submissions')),
                ('excerpt_length', models.IntegerField(default=500, help_text='The character length of the post body field displayed in RSS and preview templates.')),
                ('meta_author', models.CharField(help_text="List of authors or company/organization's name", max_length=255)),
                ('meta_keywords', models.CharField(help_text='List of keywords to help improve quality of search results', max_length=255)),
                ('meta_description', models.TextField(help_text='What the blog is about, topics, editorial line...', blank=True)),
                ('site', models.ForeignKey(related_name='+', to='sites.Site', unique=True)),
            ],
            options={
                'db_table': 'easy_blog_config',
                'verbose_name': 'app config',
                'verbose_name_plural': 'app config',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique_for_date=b'pub_date')),
                ('markup', django_markup.fields.MarkupField(default=b'markdown', max_length=255, verbose_name='markup', choices=[(b'none', b'None (no processing)'), (b'linebreaks', b'Linebreaks'), (b'markdown', b'Markdown'), (b'restructuredtext', 'reStructuredText')])),
                ('abstract', inline_media.fields.TextFieldWithInlines(default='Look at the body field for a quick Markdown cheatsheet', help_text='Check <a href="http://markable.in/file/aa191728-9dc7-11e1-91c7-984be164924a/" target=_new">Markdown syntax</a>, <a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target=_new">reStructuredText syntax</a>')),
                ('abstract_markup', models.TextField(null=True, blank=True)),
                ('body', inline_media.fields.TextFieldWithInlines(default='\nIn case you need to write headers to highlight different sections along the story, you can use headers like the following.\n\n### Header Level 3\n\nThis is a paragraph with simple content, not too long and too short, just enough to make it look like a paragraph. **This sentence has a font in bold**. *And this is in italics*. A markdown link looks like this: [Link to Google](http://www.google.com). But use HTML links at will too, specially when you want them to be opened in a different window: <A href="http://www.google.com" target="_new">Google in a new window</a>.\n\n<div style="margin:10px auto;text-align:center">Paste here your youtube or google docs content</div>\n\nThis is a regular list:\n\n* The first element of the list\n* The second element of the list\n* The third element of the list\n\nAnd this a numbered list:\n\n1. The first\n1. The second\n1. The third\n\nRemember, you can separate paragraphs with horizontal rules, by simply typing three asterisks.\n\n***\n\nSo this paragraph will be below a horizontal rule.\n\nIf you want to quote a text, as when you make a citation, use the following:\n> A small step for man a giant leap for mankind.\n\nEnjoy markdown!\n', help_text='Check <a href="http://markable.in/file/aa191728-9dc7-11e1-91c7-984be164924a/" target=_new">Markdown syntax</a>, <a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target=_new">reStructuredText syntax</a>')),
                ('body_markup', models.TextField(null=True, blank=True)),
                ('tags', tagging.fields.TagField(default=b'', max_length=255, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Draft'), (2, 'Review'), (3, 'Public')])),
                ('allow_comments', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publication date')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='Modification date')),
                ('visits', models.IntegerField(default=0, editable=False)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('site', models.ForeignKey(help_text='Site in which the entry is published', to='sites.Site')),
            ],
            options={
                'get_latest_by': 'pub_date',
                'ordering': ('-pub_date',),
                'verbose_name_plural': 'stories',
                'db_table': 'easy_blog_stories',
                'verbose_name': 'story',
                'permissions': (('can_review_stories', 'Can review stories'), ('can_see_unpublished_stories', 'Can see unpublished stories')),
            },
            bases=(models.Model,),
        ),
    ]
