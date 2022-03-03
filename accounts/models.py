from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from django_music import settings
from music.models import Song


class User(AbstractUser):

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    liked_posts = models.ManyToManyField(Song, related_name='users', blank=True)
    image = models.ImageField(upload_to='profiles', null=True, blank=True, validators=(validate_image,))
    email = models.EmailField(unique=True)

    @property
    def img(self):
        try:
            return self.image.url
        except:
            return f'/{settings.STATIC_URL}/registration/images/profile.png'

    def __str__(self):
        self.liked_posts.add()
        return self.username