from django.test import TestCase
from .models import Movie


# Create your tests here.

class MovieModelTestCase(TestCase):

    @staticmethod
    def print_info(message):
        count = Movie.objects.count()
        print(f'{message}: #all_movies={count}')

    def setUp(self) -> None:
        print('-' * 20)
        self.print_info(message='Start setUp')
        self.movie = Movie.objects.create(name='Test Movie', rating=80, year=2022)
        Movie.objects.create(name='Test Matrix', rating=90, year=1999)
        Movie.objects.create(name='Mask', rating=50, year=2008)
        self.print_info('Finish setUp')

    def test_movie_creation(self):
        # Проверка создания объекта Movie
        self.print_info('Start test_movie_creation')
        self.assertEqual(self.movie.name, 'Test Movie')
        self.assertEqual(self.movie.rating, 80)
        self.assertEqual(self.movie.year, 2022)
        self.assertEqual(self.movie.budget, 1000000)
        self.assertEqual(self.movie.slug, 'test-movie')
        self.print_info('Finish test_movie_creation')
