import os
import time
import uuid
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models

from .functions import path_to_upload_img
from .validators import validate_time_to_expired

User = settings.AUTH_USER_MODEL


class Image(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    image = models.ImageField(upload_to=path_to_upload_img, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)

    def get_filename(self):
        return Path(f'{self.image}').stem

    def __str__(self):
        return f'{self.get_filename()}'

    def get_links(self, request):
        user_tier = self.user.account_tier
        base_file = os.path.dirname(self.image.name)
        thumbnails = default_storage.listdir(base_file)[1]
        base_url = request.build_absolute_uri('/')

        thumbs_for_user = []
        for thumbnail in thumbnails:
            if 'thumb' in thumbnail:
                thumbnails_path = os.path.join(base_file, thumbnail)
                thumbs_for_user.append(base_url + settings.MEDIA_URL + thumbnails_path)

        if user_tier.is_original_file:
            thumbs_for_user.append(base_url + self.image.url)

        if user_tier.is_expiring_link and hasattr(self, 'expiring_link'):
            thumbs_for_user.append(self.expiring_link.link)

        return thumbs_for_user


class ThumbnailSize(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f'{self.width}x{self.height}'


class ExpiringLink(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    image = models.OneToOneField(Image, on_delete=models.CASCADE, unique=True, related_name='expiring_link')
    link = models.CharField(max_length=255)
    time_to_expired = models.IntegerField(validators=[validate_time_to_expired])

    def __str__(self):
        return f'{self.link}'

    def is_expired(self):
        current_time = time.time()
        return current_time > self.time_to_expired
