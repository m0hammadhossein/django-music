from datetime import timedelta
from os import remove
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
import jdatetime
from django.forms.utils import to_current_timezone


class Song(models.Model):

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='songs/covers', validators=(validate_image,))
    audio_file = models.FileField(upload_to='songs')
    duration = models.DurationField(default=timedelta)
    likes = models.PositiveIntegerField(default=0)

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using=using, keep_parents=keep_parents)
        remove(self.audio_file.path)
        remove(self.cover.path)
        return res

    def __str__(self):
        return f'{self.title}-{self.artist}'

    class Meta:
        unique_together = ('title', 'artist')
        verbose_name = 'آهنگ'
        verbose_name_plural = 'آهنگ ها'


class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField(max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childrens')
    reply_count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def jcreated_on(self):
        return jdatetime.datetime.fromgregorian(datetime=to_current_timezone(self.created_on), locale='fa_IR').strftime('%a, %d %b %Y ساعت %H:%M')

    jcreated_on.short_description = 'created on'

    class Meta:
        ordering = ('created_on',)
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'

    def __str__(self):
        return 'Comment {} by {}'.format(self.description[:15], self.user.username)