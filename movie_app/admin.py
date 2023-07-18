from django.contrib import admin
from .models import Movie
from django.db.models import QuerySet


# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'genre', 'year', 'budget', 'currency', 'rating_status']
    list_editable = ['rating', 'year', 'genre', 'currency', 'budget']
    ordering = ['-rating', 'name']
    list_per_page = 10
    actions = ['set_dollars', 'set_documentary']

    @admin.display(ordering='rating', description='Статус')
    def rating_status(self, mov: Movie):
        if mov.rating < 50:
            return 'Зачем это смотреть'
        if mov.rating < 70:
            return 'Разок можно глянуть'
        if mov.rating < 85:
            return 'Зачет!'
        return 'Топчик'

    @admin.action(description='Установить валюту доллар')
    def set_dollars(self, request, queryset: QuerySet):
        queryset.update(currency=Movie.USD)

    @admin.action(description='Установить жанр - документальный фильм')
    def set_documentary(self, request, queryset_genr: QuerySet):
        count_updated = queryset_genr.update(genre=Movie.DOCUMENTARY)
        self.message_user(request, message=f'Обновлено {count_updated} записей')


admin.site.register(Movie, MovieAdmin)  # эту привязку можно сделать через декокатор к классу @admin.register(Movie)
