from django.contrib import admin
from django.utils.html import format_html
from music.models import Song, Comment


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'likes', 'duration')
    search_fields = ('title', 'artist')

    @admin.display(description='cover')
    def image_tag(self, obj):
        return format_html('<img width=140 height=100 src="{}" style="border-radius: 10px;"/>'.format(obj.cover.url))


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('song', 'user', 'jcreated_on')
    search_fields = ('song__title', 'user__username')
    raw_id_fields = ('song', 'user', 'parent')
