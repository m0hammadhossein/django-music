from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from music.models import Comment


@receiver(post_save, sender=Comment)
def create_comment(sender, instance, created, **kwargs):
    if created:
        instance.song.comments += 1
        if instance.parent:
            instance.parent.reply_count += 1
            instance.parent.save()
        instance.song.save()


@receiver(post_delete, sender=Comment)
def create_comment(sender, instance, **kwargs):
    instance.song.comments -= 1
    if instance.parent:
        instance.parent.reply_count -= 1
        instance.parent.save()
    instance.song.save()
