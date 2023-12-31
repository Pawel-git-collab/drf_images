from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Image
from .tasks import convert_to_thumbnails


@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance: Image, **kwargs):
    convert_to_thumbnails.delay(instance.id)
