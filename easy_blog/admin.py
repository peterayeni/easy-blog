#-*- coding: utf-8 -*-

from django import forms
from django.contrib import admin

from wysihtml5.admin import AdminWysihtml5TextFieldMixin
from wysihtml5.widgets import Wysihtml5AdminTextareaWidget

from easy_blog.models import Config, Story

try:
    from easy_blog.filters import BlogAuthorsListFilter
    story_admin_list_filter = (BlogAuthorsListFilter, "status", "pub_date")
except:
    story_admin_list_filter = ("status", "pub_date")


class ConfigAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": (("site", "title"), 
                                    ("show_author", "ping_google"),
                                    "email_subscribe_url", "excerpt_length", 
                                    "stories_in_index", "comments_in_index")}),
                 ("META", {"fields": ("meta_author", "meta_description",
                                      "meta_keywords", )}),)

admin.site.register(Config, ConfigAdmin)


class StoryAdmin(AdminWysihtml5TextFieldMixin, admin.ModelAdmin):
    list_display  = ("title", "pub_date", "mod_date", 
                     "author", "status", "visits")
    list_filter   = story_admin_list_filter
    search_fields = ("title", "abstract", "body")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = ((None, {"fields": ("title", "slug",
                                    "abstract", "body",)}),
                 ("Post data", {"fields": (("site", "author", "status"), 
                                           ("allow_comments", "tags"),
                                           ("pub_date",)),}),)
    raw_id_fields = ("author",)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(StoryAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name == "abstract":
            field = forms.CharField(
                widget=Wysihtml5AdminTextareaWidget(attrs={"rows":6}))
        return field
        

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
