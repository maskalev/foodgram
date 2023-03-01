from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model.
    """
    name = models.CharField(
        verbose_name="Имя",
        max_length=256,
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=64,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        unique=True
    )
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
