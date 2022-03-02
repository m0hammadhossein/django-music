from django.db.models.signals import post_save
from django.dispatch import receiver
from music.models import Comment


@receiver(post_save, sender=Comment)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.parent:
        instance.parent.reply_count+=1
        instance.parent.save()
