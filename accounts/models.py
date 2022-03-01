from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from music.models import Song


class User(AbstractUser):

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    liked_posts = models.ManyToManyField(Song, related_name='users')
    image = models.ImageField(upload_to='profiles', null=True, blank=True, validators=(validate_image,))
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username