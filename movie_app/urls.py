from . import views
from django.urls import path

urlpatterns = [
    path('', views.show_all_movie),
    path('directors/', views.show_all_directors),
    path('actors/', views.show_all_actors),
    path('movie/<slug:slug_movie>', views.show_one_movie, name='movie-detail'),
    path('directors/<int:id_dir>', views.show_one_director, name='movie-director'),
    path('actors/<int:id_actor>', views.show_one_actor, name='movie-actor'),
]
