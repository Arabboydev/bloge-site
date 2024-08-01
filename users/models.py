from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(
        upload_to='user_img/',
        blank=True, null=True,
        default='default_img/images.png'
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

