from django.urls import path
from . import views

app_name =  'movies'

urlpatterns = [
    path('<int:movie_pk>/like/', views.like, name ='like'),
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
]
