from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="аватар",
        blank=True,
        null=True,
        help_text="Загрузите аватар",
    )

    token = models.CharField(max_length=100, verbose_name="token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_block_user", "can block user"),
        ]
