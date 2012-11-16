#-*- coding: utf-8 -*-

from django import forms
from django.contrib import admin

from wysihtml5.admin import AdminWysihtml5TextFieldMixin

from easy_blog.models import Config, Story


class ConfigAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": (("site", "title"), 
                                    ("show_author", "ping_google"),
                                    "email_subscribe_url", "excerpt_length", 
                                    "stories_in_index", "comments_in_index")}),
                 ("META", {"fields": ("meta_author", "meta_description",
                                      "meta_keywords", )}),)

admin.site.register(Config, ConfigAdmin)


class StoryAdmin(admin.ModelAdmin, AdminWysihtml5TextFieldMixin):
    list_display  = ("title", "pub_date", "author", "status", "visits")
    list_filter   = ("author", "status", "pub_date", "tags")
    search_fields = ("title", "abstract", "body")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = ((None, {"fields": ("title", "slug",
                                    "abstract", "body",)}),
                 ("Post data", {"fields": (("site", "author", "status"), 
                                           ("allow_comments", "tags"),
                                           ("pub_date", "mod_date")),}),)
    raw_id_fields = ("author",)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        if obj.author == request.user:
            return True
        if (obj.status in [2, 3] and # stories in review or published
            request.user.has_perm("easy_blog.can_review_stories")):
            return True
        return False
        
admin.site.register(Story, StoryAdmin)
