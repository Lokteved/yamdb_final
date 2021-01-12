from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    PRIVILEGED_USERS = (RoleChoices.ADMIN, RoleChoices.MODERATOR)

    email = models.EmailField(unique=True)
    bio = models.TextField(verbose_name='Описание', blank=True)
    role = models.CharField(
        verbose_name='Роль',
        max_length=128,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )


class Label(models.Model):
    name = models.CharField(max_length=512, verbose_name='Имя')
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.slug


class Category(Label):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(Label):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=1024, verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год', db_index=True)
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
        )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='%(class)ss',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='%(class)ss',
        blank=False,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Publication(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='%(class)s',
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        default=datetime.now,
    )

    class Meta:
        abstract = True


class Review(Publication):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='%(class)s',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, message='Значение рейтинга,'
                                         ' должно быть больше 1'),
            MaxValueValidator(10,  message='Значение рейтинга,'
                                           ' должно быть меньше или равно 10')]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(Publication):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='%(class)s',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
