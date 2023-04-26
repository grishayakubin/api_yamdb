from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=25,
        blank=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="titles",
        verbose_name="Автор"
    )
    slug = models.SlugField(
        unique=True
    )
    description = models.TextField(
        max_length=255
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
