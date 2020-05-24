from django.urls import path
from . import views

app_name =  'movies'

urlpatterns = [
    path('<int:movie_pk>/like/', views.like, name ='like'),
    path('', views.movie_list, name='movie_list'),
    path('sort/', views.sort, name='sort'),
    path('genre/', views.genre, name='genre'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/comments/delete/', views.comment_delete, name='comment_delete'),
]
