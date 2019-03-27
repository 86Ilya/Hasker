import os

from django.db import models
from django.contrib.auth.models import AbstractUser

from Hasker.settings import STATIC_URL

DEFAULT_AVATAR_URL = os.path.join(STATIC_URL, 'img', 'default_avatar.jpeg')


def user_avatar_path(hasker_user, filename):
    # file will be uploaded to MEDIA_ROOT/<id>_avatar.<filename extension>
    return '{}_avatar.{}'.format(hasker_user.username, filename.split(".")[-1])


class HaskerUser(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, default=None)

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return DEFAULT_AVATAR_URL
