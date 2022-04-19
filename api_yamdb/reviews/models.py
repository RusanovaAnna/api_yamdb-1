from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

MAX_SCORE = 10
MIN_SCORE = 1
SYMBOLS_LIMIT = 15


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]
    role = models.CharField(
        verbose_name='Роль', max_length=20, choices=ROLE_CHOICES, default=USER)
    bio = models.TextField(verbose_name='Биография', blank=True)

    class Meta:
        ordering = ['role']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(verbose_name='Название', max_length=20)
    slug = models.SlugField(verbose_name='Slug', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=70)
    slug = models.SlugField(verbose_name='Slug', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=150)
    year = models.PositiveSmallIntegerField(
        validators=[year_validator],
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='titles')
    genre = models.ManyToManyField(Genre)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                MAX_SCORE, f'Выберите значение от {MIN_SCORE} до {MAX_SCORE}'),
            MinValueValidator(
                MIN_SCORE, f'Выберите значение от {MIN_SCORE} до {MAX_SCORE}')
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author'
            ),
        ]

    def __str__(self):
        return self.text[:SYMBOLS_LIMIT]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:SYMBOLS_LIMIT]
