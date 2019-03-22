from django.db import models
from django.contrib.auth.models import AbstractUser


def user_avatar_path(hasker_user, filename):
    # file will be uploaded to MEDIA_ROOT/<id>_avatar.<filename extension>
    return '{}_avatar.{}'.format(hasker_user.username, filename.split(".")[-1])


class HaskerUser(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, default='default_avatar.jpeg')
