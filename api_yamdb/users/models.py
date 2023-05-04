from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models import CharField

from .constants import Role
from .validators import not_me_username_validator, username_validator

CONF_CODE_MAX_LEN: int = 150
EMAIL_MAX_LEN: int = 254
ROLE_MAX_LEN: int = 30
USERNAME_MAX_LEN: int = 150


class User(AbstractUser):
    """Модель Пользователя."""

    ROLE_CHOICES = (
        (Role.USER, "user"),
        (Role.MODERATOR, "moderator"),
        (Role.ADMIN, "admin"),
    )

    first_name = models.CharField(
        "Имя", blank=True, max_length=CONF_CODE_MAX_LEN
    )
    bio = models.TextField(
        "Биография", blank=True, help_text="Здесь напишите о себе"
    )
    confirmation_code = models.CharField(
        "Код подтверждения", blank=True, max_length=CONF_CODE_MAX_LEN
    )
    email = models.EmailField(
        "Адрес эл. почты",
        max_length=EMAIL_MAX_LEN,
        unique=True,
        help_text="Введите адрес электронной почты",
    )
    role = models.CharField(
        "Роль пользователя",
        choices=ROLE_CHOICES,
        max_length=ROLE_MAX_LEN,
        default="user",
        help_text="Выберите роль пользователя",
    )
    username = models.CharField(
        "Username",
        max_length=USERNAME_MAX_LEN,
        unique=True,
        help_text="Введите имя пользователя",
        validators=[not_me_username_validator, username_validator],
    )

    def email_user(
        self,
        message,
        subject="Регистрация",
        from_email="yamdb@gmail.com",
        **kwargs
    ):
        send_mail(
            subject,
            message,
            from_email,
            [self.email],
            fail_silently=False,
            **kwargs
        )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self) -> CharField:
        return self.username

    def save(self, *args, **kwargs):
        if self.role == Role.MODERATOR:
            self.is_staff = True
        if self.role == Role.ADMIN:
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == Role.ADMIN
