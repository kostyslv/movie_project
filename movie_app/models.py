from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class DressingRoom(models.Model):
    floor = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return f'{self.floor} {self.number}'


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    director_email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_url(self):
        return reverse('movie-director', args=[self.id])


class Actor(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE)
    dressing = models.OneToOneField(DressingRoom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.gender == self.MALE:
            return f'Актер {self.first_name} {self.last_name}'
        else:
            return f'Актриса {self.first_name} {self.last_name}'

    def get_url(self):
        return reverse('movie-actor', args=[self.id])


class Movie(models.Model):
    DRAMA = 'драма'
    COMEDY = 'комедия'
    DOCUMENTARY = 'документальный'
    THRILLER = 'триллер'
    CURRENCY_GENRE = [
        (DRAMA, 'drama'),
        (COMEDY, 'comedy'),
        (DOCUMENTARY, 'documentary'),
        (THRILLER, 'thriller')
    ]

    EUR = 'EUR'
    USD = 'USD'
    RUB = 'RUB'
    CURRENCY_CHOISES = [
        (EUR, 'euro'),
        (USD, 'dollar'),
        (RUB, 'ruble')
    ]

    name = models.CharField(max_length=40)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    genre = models.CharField(max_length=15, choices=CURRENCY_GENRE, default=DRAMA)
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(default=1000000, validators=[MinValueValidator(1)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOISES, default=RUB)
    slug = models.SlugField(default='', null=False, db_index=True)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.rating}%'

    def get_url(self):
        return reverse('movie-detail', args=[self.slug])
