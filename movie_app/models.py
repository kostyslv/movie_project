from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
    rating = models.IntegerField()
    genre = models.CharField(max_length=15, choices=CURRENCY_GENRE, default=DRAMA)
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(default=1000000)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOISES, default=RUB)
    slug = models.SlugField(default='', null=False, db_index=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.rating}%'

    def get_url(self):
        return reverse('movie-detail', args=[self.slug])
