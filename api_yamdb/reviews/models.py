import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

MAX_SCORE = 10
MIN_SCORE = 1
SYMBOLS_LIMIT = 15


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    # password = None
    last_login = None
    date_joined = None
    role = models.CharField(max_length=20, choices=ROLES)
    bio = models.TextField(blank=True)
    confirmation_code = models.TextField(blank=True, null=True)


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=150)
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(datetime.datetime.now().year)]
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='titles_cats')
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review_ttl')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review_auth')
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='title_author')
        ]

    def __str__(self):
        return self.text[:SYMBOLS_LIMIT]


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment_auth')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:SYMBOLS_LIMIT]
