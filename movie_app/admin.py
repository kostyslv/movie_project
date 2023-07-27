from django.contrib import admin
from .models import Movie, Director, Actor, DressingRoom
from django.db.models import QuerySet



# Register your models here.

admin.site.register(Director)
admin.site.register(Actor)
# admin.site.register(DressingRoom)

@admin.register(DressingRoom)
class DressingRoomAdmin(admin.ModelAdmin):
    list_display = ['floor', 'number', 'actor']


class RatingFilter(admin.SimpleListFilter):
    title = 'Фильтр по рейтингу'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<40', 'Низкий'),
            ('от 40 до 59', 'Средний'),
            ('от 60 до 79', 'Высокий'),
            ('>=80', 'Высший'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value()=='<40':
            return queryset.filter(rating__lt=40)
        if self.value()=='от 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        if self.value()=='от 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        if self.value()=='>=80':
            return queryset.filter(rating__gte=80)

class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'director', 'genre', 'year', 'budget', 'currency', 'rating_status']
    # exclude = ['slug']
    prepopulated_fields = {'slug': ('name', )}
    list_editable = ['rating', 'year', 'genre', 'director', 'currency', 'budget']
    ordering = ['-rating', 'name']
    list_per_page = 10
    filter_horizontal = ['actors']
    actions = ['set_dollars', 'set_documentary']
    search_fields = ['name__startswith']
    list_filter = ['name', 'genre', RatingFilter]

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
