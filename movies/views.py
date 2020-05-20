from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Prefetch
from .models import Movie
from accounts.models import UserProfile

from django.conf import settings
import requests
import random

# main page - 영화 전체 목록
def home(request):
    movies = Movie.objects.order_by('-release_date')[:10]
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            recommand_movies = list(Movie.objects.filter(genres__in=profile.favorites))
            
        except UserProfile.DoesNotExist:
            profile = None
            recommand_movies = list(Movie.objects.all())
        recommand_movies = random.sample(recommand_movies, 10)
        context = {
                'recommand_movies': recommand_movies,
                'movies': movies,
            }
        return render(request, 'movies/home.html', context)
    context = {
            'movies': movies,
        }
    return render(request, 'movies/home.html', context)
    

def movie_list(request):
    pass
# # 전체 영화들 보기
# def movie_list(request):
#     movies = Movie.objects.order_by('-vote_average')
#     context = {
#         'movies': movies,

#     }
#     return render(request, 'movies/movie_list.html', context)

def like(request):
    pass

# 영화별 상세보기 - 해당 영화 리뷰출력
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, id=movie_pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/movie_detail.html', context)